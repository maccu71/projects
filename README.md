Here you will find 5 small projects:

<br/><br/> 

1) `init-containers-usage` - a helm package that illustrates how to use init-containers in Kubernetes cluster. 

![obraz](https://github.com/maccu71/projects/assets/51779238/d982af6a-e8ef-4a85-b30a-4619db6070a1)

To install this deployment with its service you need to:
1) have working Kubernetes cluster eg. Minikube and Helm package installed
2) `helm install my-release https://raw.githubusercontent.com/maccu71/projects/master/init-containers-usage-1.0.0.tgz`
3) you'll see the picture from NASA server on your browser:   `localhost:$(kubectl get service my-release -o jsonpath='{.spec.ports[*].nodePort}'|jq)`  
OR if you use Minikube just: `minikube service my-release`

Init containers in Kubernetes are lightweight, transient containers that run and complete before the main application containers start. They are designed to perform initialization tasks, setup, or any necessary preparations before the main application containers in a pod begin running.

Key points about init containers:

- Initialization Tasks: Init containers are commonly used to perform tasks such as fetching necessary resources, setting up configurations, or waiting for external services to be ready.

- Sequential Execution: Init containers in a pod are executed in order, one after the other. Each init container must complete successfully before the next one starts.

- Separation of Concerns: They allow for the separation of concerns between the initialization process and the main application logic. This can be particularly useful for scenarios where dependencies need to be in place before the main application starts.

- Transient Nature: Once an init container completes its task, it exits. It doesn't run alongside the main application containers during the pod's lifecycle.

In this example, we could use a ConfigMap with a Bash script (what would be the proper way of handling more complicated Bash scripts), but the example is intended to demonstrate the behavior of consecutive init containers."

This version clarifies the potential use of a ConfigMap with a Bash script for more complex scenarios while emphasizing the primary purpose of the example, which is to showcase the behavior of sequential init containers

<br/><br/> 

2) `stacje.py` - an application that searches for available radio stations, allows you to select one from the list, starts it, and shows the name of the artist and song. This is a really nice app that you can launch directly from your Linux console.

![obraz](https://github.com/maccu71/projects/assets/51779238/ed8fc9dc-b2ab-41fe-a0d5-b0b1d88a57f6)

<br/><br/> 

3) `cwicz.py` - created to track and backup my running results and display them on a nice graph, this application utilizes various Python modules.
   
![obraz](https://github.com/maccu71/projects/assets/51779238/4cd59ca3-d49e-435e-a71b-6646fa46218e)

<br/><br/> 

4) `cleaner.yml` - kubernetes manifest intended to clean unnecessary resources from kubernetes cluster (use with caution)

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

5) `sonda-readiness-tcp.yml` - A Kubernetes manifest showcasing the capabilities of a readinessProbe, a powerful feature ensuring the operational readiness of containers. 

In this case, the readinessProbe is utilized to validate the availability of my local NFS service before bringing to life the container

A readinessProbe in Kubernetes serves as a mechanism to determine whether a container is ready to handle incoming traffic. It plays a mportant role in scenarios where readiness of a service or resource is crucial before allowing the container to receive requests. In this context, the readinessProbe checks the status of an NFS service, ensuring its activation and functionality before proceeding with the creation of the container. This approach enhances the reliability of the containerized application, preventing potential issues that may arise if the required services are not adequately prepared.

You start this deployment by issuing: `kubectl apply -f https://raw.githubusercontent.com/maccu71/projects/master/sonda-readiness-tcp.yml.yml` but probably you don't have configured NFS on provided address/path..

- Lets assume the situation when our NFS is not ready yet. The readinessProbe will check the TCP-connection on standard NFS port (2049) and doesn't show positive outcome. In that case ReplicaSet will refrain from launching the Pod.
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


- When obstacles are overcome and the readinessProbe gives positive outcome (eg. service nfs-server is restarted and working), the creation of container proceed.
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



