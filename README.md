Here are some projects related to my interests, including IaC, Kubernetes, Ansible, and Python programming.

<br/><br/> 

1) `memory-restriction.yml` - Explores the concept of resource allocation and memory restriction in Kubernetes

Here, you can find a Kubernetes manifest showcasing the idea of constraining allocated available resources by specifying their limits, in this case, memory. Running containers without specifying limits can lead to issues. 
Bugs in applications, failed services, or memory leaks can cause an increase in memory usage, potentially using up all available resources on a Kubernetes node. Thus, the idea of constraining allocated resources.

Start the deployment by issuing: 
`kubectl apply -f https://raw.githubusercontent.com/maccu71/projects/master/memory-restriction.yml`

In this example, we deploy a single container and a package that stresses the container's memory. It allocates an additional 20Mi of memory every 30 seconds. To safeguard the resources of our Kubernetes node, we introduce memory restrictions in the container's spec. It looks like this:

```
spec:
  containers:
    - name: vehicle
      image: ubuntu:latest
      resources:
        limits:
          memory: 80Mi
```

We will increase allocated memory until it reaches the memory limit. 
Can you guess what happens in that case?
```
currently: 20M
stress: info: [234] dispatching hogs: 0 cpu, 0 io, 1 vm, 0 hdd
stress: info: [234] successful run completed in 25s
currently: 40M
stress: info: [236] dispatching hogs: 0 cpu, 0 io, 1 vm, 0 hdd
stress: info: [236] successful run completed in 25s
currently: 60M
stress: info: [238] dispatching hogs: 0 cpu, 0 io, 1 vm, 0 hdd
stress: info: [238] successful run completed in 25s
currently: 80M
stress: info: [240] dispatching hogs: 0 cpu, 0 io, 1 vm, 0 hdd
stress: FAIL: [240] (416) <-- worker 241 got signal 9
stress: WARN: [240] (418) now reaping child worker processes
stress: FAIL: [240] (422) kill error: No such process
stress: FAIL: [240] (452) failed run completed in 0s
```
```
kubectl get pods --watch
NAME                      READY   STATUS    RESTARTS   AGE
memory-699b66468f-mm7qx   0/1     Pending   0          0s
memory-699b66468f-mm7qx   0/1     Pending   0          0s
memory-699b66468f-mm7qx   0/1     ContainerCreating   0          0s
memory-699b66468f-mm7qx   1/1     Running             0          3s
memory-699b66468f-mm7qx   0/1     OOMKilled           0          85s      <====
memory-699b66468f-mm7qx   1/1     Running             1 (3s ago)   87s
memory-699b66468f-mm7qx   0/1     OOMKilled           1 (85s ago)   2m49s
memory-699b66468f-mm7qx   0/1     CrashLoopBackOff    1 (17s ago)   3m5s
memory-699b66468f-mm7qx   1/1     Running             2 (19s ago)   3m7s
memory-699b66468f-mm7qx   0/1     OOMKilled           2 (100s ago)   4m28s
memory-699b66468f-mm7qx   0/1     CrashLoopBackOff    2 (12s ago)    4m40s
memory-699b66468f-mm7qx   1/1     Running             3 (28s ago)    4m56s
```

Now, Kubernetes will be restarting the pod due to OOMKilled events when the allocated memory reaches its limit. 
What happens then with the deployment itself? We can ask.

Your guess is right; Kubernetes will be restarting the pod repeatedly. 
Surely, Kubernetes employs an exponential backoff mechanism, substantially increasing the time between each failure. 
This helps prevent overwhelming the system with many restarts and unnecessary resource stress.

However, in my opinion, it's not an fully automatic solution, leaving room for improvement for Kubernetes developers. 
One can imagine a situation where the default immutable `restartPolicy: Always` can be changed to, for example, `3`.

Now you can kick out the deployment by:
`kubectl delete -f https://raw.githubusercontent.com/maccu71/projects/master/memory-restriction.yml`

<br/><br/> 

2) `init-containers-usage` - a helm package that illustrates how to use init-containers in Kubernetes cluster. 

![obraz](https://github.com/maccu71/projects/assets/51779238/d982af6a-e8ef-4a85-b30a-4619db6070a1)

To install this deployment with its service you need to:
- have working Kubernetes cluster eg. Minikube and Helm package installed
- `helm install my-release https://raw.githubusercontent.com/maccu71/projects/master/init-containers-usage-1.0.0.tgz`
- you'll see the picture from NASA server on your browser:   `localhost:$(kubectl get service my-release -o jsonpath='{.spec.ports[*].nodePort}'|jq)`  
OR if you use Minikube just: `minikube service my-release`

Init containers in Kubernetes are lightweight, transient containers that run and complete before the main application containers start. They are designed to perform initialization tasks, setup, or any necessary preparations before the main application containers in a pod begin running.

Key points about init containers:

- Initialization Tasks: Init containers are commonly used to perform tasks such as fetching necessary resources, setting up configurations, or waiting for external services to be ready.

- Sequential Execution: Init containers in a pod are executed in order, one after the other. Each init container must complete successfully before the next one starts.

- Separation of Concerns: They allow for the separation of concerns between the initialization process and the main application logic. This can be particularly useful for scenarios where dependencies need to be in place before the main application starts.

- Transient Nature: Once an init container completes its task, it exits. It doesn't run alongside the main application containers during the pod's lifecycle.

This version clarifies the potential use of a ConfigMap with a Bash script for more complex scenarios while emphasizing the primary purpose of the example, which is to showcase the behavior of sequential init containers

<br/><br/> 

2) `stacje.py` - an application written in Python that searches for available radio stations, allows you to select one from the list, starts it, and shows the name of the artist and song. This is a really nice app that you can launch directly from your Linux console.

![obraz](https://github.com/maccu71/projects/assets/51779238/ed8fc9dc-b2ab-41fe-a0d5-b0b1d88a57f6)

<br/><br/> 

4) `cwicz.py` - a Python program created to track and backup my running results and display them on a nice graph, this application utilizes various Python modules.
   
![obraz](https://github.com/maccu71/projects/assets/51779238/4cd59ca3-d49e-435e-a71b-6646fa46218e)

<br/><br/> 

5) `cleaner.yml` - kubernetes manifest intended to clean unnecessary resources from kubernetes cluster (use with caution)

You start deployment by: `kubectl apply -f https://raw.githubusercontent.com/maccu71/projects/master/cleaner.yml`

The application is designed to manage and clean up resources within a Kubernetes cluster. It runs as a script or containerized process within a Kubernetes pod, providing functionality to delete specified deployments, services, and even trigger the self-deletion. Clean the enviroment without deleting deployments and services individually.

Key Components:

   a) Cleaner Script/Container
   b) Kubernetes RBAC Rules

Use Case Scenario:

When periodic resource cleanup is required in the Kubernetes cluster, the Cleaner application is deployed to automate the process. It ensures that only the specified services and deployments are retained, providing a streamlined and controlled environment.

It's important to note that this isn't a production solution that involves a ready-to-go image. Instead, it is intended to showcase the RBAC possibilities.
To delete leftovers (RBAC rules) you can proceed with a command:
`kubectl delete -f https://raw.githubusercontent.com/maccu71/projects/master/cleaner.yml`


<br/><br/> 

6) `sonda-readiness-tcp.yml` - A Kubernetes manifest showcasing the capabilities of a readinessProbe, a powerful feature ensuring the operational readiness of containers. 

In this case, the readinessProbe is utilized to validate the availability of my local NFS service before bringing to life the container

A readinessProbe in Kubernetes serves as a mechanism to determine whether a container is ready to handle incoming traffic. It plays a mportant role in scenarios where readiness of a service or resource is crucial before allowing the container to receive requests. In this context, the readinessProbe checks the status of an NFS service, ensuring its activation and functionality before proceeding with the creation of the container. This approach enhances the reliability of the containerized application, preventing potential issues that may arise if the required services are not adequately prepared.

You start this deployment by issuing: `kubectl apply -f https://raw.githubusercontent.com/maccu71/projects/master/sonda-readiness-tcp.yml.yml` but probably you don't have configured NFS on provided address/path..

- Let's assume a situation where our NFS is not ready yet. The readinessProbe will check the TCP connection on the standard NFS port (2049) and, if it doesn't yield a positive outcome, the ReplicaSet will refrain from launching the Pod.

```
kubectl get po,deploy
NAME                            READY   STATUS              RESTARTS   AGE
pod/sonda-tcp-7bfcd95db-hv87v   0/1     ContainerCreating   0          11s

NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/sonda-tcp   0/1     1            0           11s

kubectl describe pod $(kubectl get po -o jsonpath='{.items[].metadata.name}')|grep -A5 Conditions
Conditions:
  Type              Status
  Initialized       True
  Ready             False    <===
  ContainersReady   False    <===
  PodScheduled      True
```

- Once obstacles are overcome, and the readinessProbe indicates a positive outcome (for example, if the NFS server service is restarted and working), the container creation will proceed.

```
kubectl describe pod $(kubectl get po -o jsonpath='{.items[].metadata.name}')|grep -A5 Conditions`
Conditions:
   Type              Status
   Initialized       True
   Ready             True    <===
   ContainersReady   True    <===
   PodScheduled      True

kubectl get deploy,po
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/sonda-tcp   1/1     1            1           9m35s

NAME                            READY   STATUS    RESTARTS   AGE
pod/sonda-tcp-7bfcd95db-hv87v   1/1     Running   0          9m35s
```

Rediness Probe is seen in Minikube as well. 
![obraz](https://github.com/maccu71/projects/assets/51779238/de056979-0c0f-4860-aa6a-0e14aeba2f2e)


