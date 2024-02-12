Here are some projects related to my interests, including IaC, Kubernetes, Ansible or Python programming.

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
One can imagine a situation where the default immutable `restartPolicy: Always` can be changed to some value after that Kubernetes ceased to create new Pod instances.

Now you can kick out the deployment by:
`kubectl delete -f https://raw.githubusercontent.com/maccu71/projects/master/memory-restriction.yml`

<br/><br/> 

2) `init-containers-usage` - a helm package that illustrates the concept of init-containers in Kubernetes cluster. 

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

2) `stacje.py` - an application written in Python 3 that searches for available radio stations, allows you to select one from the list, starts it, and shows the name of the artist and song. This is a really nice app that you can launch directly from your Linux console. Start the program in your linux console by issuing: `python3 stacje.py` or `./stacje.py`

<br/><br/> 

4) `cwicz.py` - a Python program created to track and backup my running results and display them on a nice graph, this application utilizes various Python modules.
![obraz](https://github.com/maccu71/projects/assets/51779238/887d3e3c-b59d-4a1c-bac3-c4e738d7160f)

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
```
```
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
```
```
kubectl get deploy,po
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/sonda-tcp   1/1     1            1           9m35s

NAME                            READY   STATUS    RESTARTS   AGE
pod/sonda-tcp-7bfcd95db-hv87v   1/1     Running   0          9m35s
```

Rediness Probe is seen in Minikube as well. 
![obraz](https://github.com/maccu71/projects/assets/51779238/de056979-0c0f-4860-aa6a-0e14aeba2f2e)

6) `cpu-restriction.yml` - a manifest that serves as a practical demonstration of CPU restrictions implemented both at the deployment specification and the namespace quota level in Kubernetes.
  
You start deployment by: `kubectl apply -f https://raw.githubusercontent.com/maccu71/projects/master/cpu-restriction.yml`
   
We've already learned that deploying instances without memory and CPU restrictions isn't prudent. They may, in certain scenarious, consume all available resources, jeopardizing the stability of the entire cluster.

Let's continue discussing restrictions on our workload in Kubernetes further, this time focusing on CPU and delving deeper into the broader concept of resource restriction.

Now, we'll attempt to set CPU restrictions that apply to several components. To do this, we'll create the new namespace, a limited segment of the Kubernetes environment. This allows us to isolate resources from other components in our Kubernetes cluster, providing a clear vision.

kubectl apply -f cpu-restriction.yml

This command is meant to:

- Create a new namespace named 'new' - be sure this name hasn't been used previously!
- Apply restrictions to our namespace (Quota).
- Create a simple deployment with one pod.

We're applying the following constraints on our namespace (Quota) in the cpu-restriction.yml file:
```
spec:
  hard:
    requests.cpu: "250m"  
    limits.cpu: "500m"
```
And CPU restrictions in the deployment specification:
```
resources:
  limits:
    cpu: 60m
  requests:
    cpu: 50m
```
We can see the CPU consumption of our pod:
```
kubectl top pod -n new
NAME                              CPU(cores)   MEMORY(bytes)   
cpu-restriction-bf756bcc6-xk6cd   2m           0Mi
```
Even though the existing Pod uses only 2 milliCores, the system shows different values:
```
kubectl describe quota -n new
Name:         resource-quota
Namespace:    new
Resource      Used  Hard
--------      ----  ----
limits.cpu    60m   500m
requests.cpu  50m   250m
```
This led us to the conclusions about:
- Request and Limits in Quotas (on a certain Namespace). These values provide information about HARD unsurpassable limits, meaning those that cannot be exceeded - available resources for a certain namespace.
- Requests and Limits set in deployment/pod specification. These values are meant to ALLOCATE, in other words, RESERVE a certain amount of CPU milliCores in a given Namespace.

An attempt to exceed these 'HARD' limits (limits.cpu, requests.cpu) will result in denial of new resources. For example, if we try to scale the existing deployment by adding new pods and thus allocating more CPU than is possible, regardless when it comes to Requests or Limits:

`kubectl scale deploy/cpu-restriction -n new --replicas=6`
```
kubectl get resourcequota -n new
NAME             AGE     REQUEST                   LIMIT
resource-quota   3h10m   requests.cpu: 250m/250m   limits.cpu: 300m/500m
```
```
kubectl get pod/cpu-restriction-bf756bcc6-42lf8 -n new -o jsonpath='{.spec.containers[*].resources}'|jq
{
  "limits": {
    "cpu": "60m"
  },
  "requests": {
    "cpu": "50m"
  }
}
```
```
kubectl get deploy -n new
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
cpu-restriction   5/6     5            5           26m   <==== discrepency
```

Exactly the 6th pod won't be created because available cpu.requests (HARD limit from quota on the namespace, e.g., requests.cpu = 250m and 6(pods)*50m(cpu.requests in the pod) = 300m. Limit has already been reached.

This occurs even though the real CPU Pod consumption is minimal (around 2 milliCores)
```
kubectl describe quota -n new
NAME                              CPU(cores)   MEMORY(bytes)           
cpu-restriction-bf756bcc6-m2x9b   2m           0Mi             
```
```
kubectl describe quota -n new
Name:         resource-quota
Namespace:    new
Resource      Used  Hard
--------      ----  ----
limits.cpu    300m  500m
requests.cpu  250m  250    <=== no CPU for another reservation
```

The other scenario is when deployed applications must compete for available CPU and memory resources in the cluster above specified CPU Request (in deployment spec).

Now, you may want to change the peaceful command line.. in cpu-restriction.yml 
```
      containers:
        - name: cpu
          image: ubuntu:latest
          command: ['sh','-c','while true; do date & sleep 2; done']
```
..with something more CPU-intensive, I mean a few bash line making it much more CPU-intensive. It is intended to calculate the PI number with high accuracy using binary calcuator (bc).  
`command: ['sh','-c','apt update && apt-get install bc -y && while true; do echo "scale=1000; a(1)*4" | bc -l & sleep 1; done']`

Restart the deployment with `kubectl apply -f cpu-restriction -n new` this time locally.
Now, we are not constraint with quota in the namespace (because we have enough CPU resources), but CPU contraints in our deployment spec:  

```
kubectl get pod $(kubectl get po -n new -o jsonpath='{.items[*].metadata.name}') -n new -o jsonpath='{.spec.containers[*].resources}'|jq
{
  "limits": {
    "cpu": "60m"  <=== HARD limit
  },
  "requests": {
    "cpu": "50m"  <=== SOFT limit
  }
}
```
```
kubectl  top pod -n new
NAME                               CPU(cores)   MEMORY(bytes)
cpu-restriction-5b6988d7dd-nl5h2   60m          87Mi    <=== CPU exceded cpu.requests but cannot exceed cpu.limits from deployment spec  
```

The exercise also depends on the performance of our processor. Your CPU unit is probably much agile that mine, thus the results can be different. 
You might want to experiment with Limits and Request in the specification as well as variable 'scale' in a container command. Making it bigger will stress the CPU unit much more. 

To sum it up - we come to the following conclusions:
- Requests - are considered as vital information in the deployment/pod specification on how many resources should be reserved. They are SOFT values. It means they can be exceedeed IF some application is more demanding in terms of CPU/memory AND there are free available resources in a namespace. 
- Limits - impassable, final, HARD limits. The application will not be able to exceed these values (it will be throttled).

To kick out all resources you might issue : `kubectl delete -f https://raw.githubusercontent.com/maccu71/projects/master/cpu-restriction.yml` or simply: `kubectl delete --all -n new`

