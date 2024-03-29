Here are some projects related to my interests, including IaC, Kubernetes, Ansible or Python programming.

<br/><br/> 

**1) `memory-restriction.yml` - Explores the concept of resource allocation and memory restriction in Kubernetes**

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

**2) `cpu-restriction.yml` - a manifest that serves as a practical demonstration of CPU restrictions implemented both at the deployment specification and the namespace quota level in Kubernetes.**

At the very beginning, let's dive into `the concept of milliCores` in Kubernetes. Essentially, it is designed to provide fine-grained control over available CPU resources. In this context, a full core, which is traditionally measured in gigabytes (1G), is divided into 1000 particles known as milliCores. This division allows for more precise and granular constraints on resource allocation.

Moreover, the use of milliCores offers a more user-friendly representation. For instance, it is much clearer to express resource usage as 50 milliCores rather than 0.05 cores. This not only enhances clarity but also makes resource management more intuitive and visually appealing.

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
We can see the CPU consumption of our Pod:
```
kubectl top pod -n new
NAME                              CPU(cores)   MEMORY(bytes)   
cpu-restriction-bf756bcc6-xk6cd   2m           0Mi
```
Even though the existing Pod uses only 2 milliCores, the system reserved for it the whooping 50 milliCores:
```
kubectl describe quota -n new
Name:         resource-quota
Namespace:    new
Resource      Used  Hard
--------      ----  ----
limits.cpu    60m   500m
requests.cpu  50m   250m
```
This led us to the conclusions about Quotas in a namespaces:
- Request and Limits in Quotas. These values provide information about HARD unsurpassable limits, meaning those values cannot be exceeded - there are available resources for a certain namespace.
- Requests and Limits set in deployment/pod specification. These values are meant to ALLOCATE, in other words, RESERVE a certain amount of CPU milliCores in a given Namespace.

An attempt to exceed these 'HARD' limits (limits.cpu, requests.cpu) will result in denial of creation new resources. For example, if we try to scale the existing deployment by adding new pods and thus allocating more CPU than is possible, regardless when it comes to Requests or Limits:

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
kubectl  top pod -n new
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
<br/><br/>

The other scenario is when deployed applications must compete for available CPU and memory resources in the cluster above specified CPU Request (in deployment spec).

Now, you may want to change the peaceful 
`['sh','-c','while true; do date & sleep 2; done']` 
in cpu-restriction.yml 
 
```
      containers:
        - name: cpu
          image: ubuntu:latest
          command: ['sh','-c','while true; do date & sleep 2; done']
```
<br/>
..with one bash line that causes the whole thing more CPU-intensive:   

```
command: ['sh','-c','apt update && apt-get install bc -y && while true; do echo "scale=1000; a(1)*4" | bc -l & sleep 1; done']
```

<br/>
By the way, It is a simple way aimed to calculate the PI number with high accuracy using a basic calculator (bc).

Restart the deployment with `kubectl apply -f cpu-restriction -n new` this time locally.
Now, we are not constraint with quota in the namespace (we have enough CPU resources), but CPU contraints in our deployment spec:  

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
The exercise also depends on the performance of our processors. Your CPU unit is likely much more agile than mine, so the results may differ. You can experiment with the 'Limits' and 'Requests' in the specification, as well as the 'scale' variable in the container command. Increasing the 'scale' will stress the CPU unit more.

To sum it up, we arrive at the following conclusions:

- 'Requests' are considered vital information in the deployment/pod specification, indicating how many resources should be reserved. They are SOFT values, meaning they can be exceeded if some application is more demanding in terms of CPU/memory, and there are free available resources in a namespace.
- 'Limits' are impassable, final, HARD limits. The application will not be able to exceed these values; it will be throttled."

<br/><br/> 

You might want to kick out all resources by: `kubectl delete -f https://raw.githubusercontent.com/maccu71/projects/master/cpu-restriction.yml` or simply: `kubectl delete --all -n new` but let's dive into the particularies of `Quality of Service - QoS` within our deployed pods, tightly linked with mentioned CPU and memory restrictions.

We're dealing with three amigos here: `BestEffort, Burstable, and Guaranteed`. Let's break down each one and unravel their differences.

`Guaranteed`

In this VIP category, CPU and memory values are like best buds:
```
resources:
  limits:
    cpu: 100m
    memory: 200Mi
  requests:
    cpu: 100m
    memory: 200Mi
```
When you run `kubectl describe pod -n new | grep QoS`, you'll see it proudly having the title `QoS Class: Guaranteed`. The best service guaranteed; Kubernetes treats these pods with the utmost respect, messing with them only if absolutely necessary. These pods have a fixed amount of resources allocated to them. They won't get more, and they won't get less, ensuring a stable environment.

`Burstable`

This is the flexible friend in the group. The CPU and/or memory limits and requests are different:
```
resources:
  limits:
    cpu: 60m
    memory: 200Mi
  requests:
    cpu: 50m
    memory: 100Mi
```
Peek at `kubectl describe pod -n new | grep QoS`, and you'll find it having the `QoS Class: Burstable` label. Pods in this category get a minimum amount of resources but can use more if available (until limits - if specified).

`- BestEffort`

Here's the wild card. Whether you skip specifying CPU/memory altogether (not recommended, by the way), or if the requests and limits don't match, you're in BestEffort territory:

Example situations falling into BestEffort:
- CPU/memory not specified at all (not cool)
- CPU.requests and CPU.limits mismatch
- Memory.requests and Memory.limits mismatch

When you `kubectl get pod -n new -o yaml | grep qosClass`, it shows `qosClass: BestEffort`. Pods in this category get whatever resources are available but it's the low-key player; when resources get tight, these pods are "released" first, giving priority to their Guaranteed and Burstable counterparts. So they may struggle if resources are constrained.


<br/><br/>

**3) `init-containers-usage` - a helm package that illustrates the concept of init-containers in Kubernetes cluster.** 

![obraz](https://github.com/maccu71/projects/assets/51779238/d982af6a-e8ef-4a85-b30a-4619db6070a1)

To install this deployment with its service you need to:
- have working Kubernetes cluster eg. Minikube and Helm package installed
- `helm install my-release https://raw.githubusercontent.com/maccu71/projects/master/init-containers-usage-1.0.0.tgz`
- you'll see the picture from NASA server on your browser:   `localhost:$(kubectl get service my-release -o jsonpath='{.spec.ports[*].nodePort}'|jq)`  
OR if you use Minikube just: `minikube service my-release`

Init containers in Kuberneteso are lightweight, transient containers that run and complete before the main application containers start. They are designed to perform initialization tasks, setup, or any necessary preparations before the main application containers in a pod begin running.

```
spec:
  initContainers:
    - name: init-1
      image: ubuntu:latest
      command: ['sh','-c','apt update && apt-get install wget -y  && wget -O /data/one.jpg -q "https://apod.nasa.gov/apod/image/2312/ArcticNight_Cobianchi_2048.jpg"']
      volumeMounts:
        - name: html
          mountPath: /data
    - name: init-2
      [...]

  containers: 
    - name: web
      image: nginx:latest
```

Key points about init containers:

- Initialization Tasks: Init containers are commonly used to perform tasks such as fetching necessary resources, setting up configurations, or waiting for external services to be ready.

- Sequential Execution: Init containers in a pod are executed in order, one after the other. Each init container must complete successfully before the next one starts.

- Separation of Concerns: They allow for the separation of concerns between the initialization process and the main application logic. This can be particularly useful for scenarios where dependencies need to be in place before the main application starts.

- Transient Nature: Once an init container completes its task, it exits. It doesn't run alongside the main application containers during the pod's lifecycle.

This version clarifies the potential use of a ConfigMap with a Bash script for more complex scenarios while emphasizing the primary purpose of the example, which is to showcase the behavior of sequential init containers

<br/><br/> 

**4) `stacje.py` - an application written in Python 3 that searches for available radio stations, allows you to select one from the list, starts it, and shows the name of the artist and song.**

 This is a really nice app that you can launch directly from your Linux console. Start the program in your linux console by issuing: 
`python3 stacje.py` 
or just 
`./stacje.py`

<br/><br/> 

**5) `cwicz.py` - a Python program created to track and backup my running results and display them on a nice graph, this application utilizes various Python modules.**
![obraz](https://github.com/maccu71/projects/assets/51779238/887d3e3c-b59d-4a1c-bac3-c4e738d7160f)

<br/><br/> 

**6) `cleaner.yml` - kubernetes manifest intended to clean unnecessary resources from kubernetes cluster (use with caution)**

You start deployment by: `kubectl apply -f https://raw.githubusercontent.com/maccu71/projects/master/cleaner.yml`

The application is designed to manage and clean up resources within a Kubernetes cluster. It runs as a script or containerized process within a Kubernetes pod, providing functionality to delete specified deployments, services, and even trigger the self-deletion. Clean the enviroment without deleting deployments and services individually.

Key Components:

- Cleaner Script/Container
- Kubernetes RBAC Rules (we say about them later)

Use Case Scenario:

When periodic resource cleanup is required in the Kubernetes cluster, the Cleaner application is deployed to automate the process. It ensures that only the specified services and deployments are retained, providing a streamlined and controlled environment.

It's important to note that this isn't a production solution that involves a ready-to-go image. Instead, it is intended to showcase the RBAC possibilities.
To delete leftovers (RBAC rules) you can proceed with a command:
`kubectl delete -f https://raw.githubusercontent.com/maccu71/projects/master/cleaner.yml`


<br/><br/> 

**7) `sonda-readiness-tcp.yml` - A Kubernetes manifest showcasing the capabilities of a readinessProbe, a powerful feature ensuring the operational readiness of containers.** 

In this case, the readinessProbe is utilized to validate the availability of my local NFS service before bringing to life the container

A readinessProbe in Kubernetes serves as a mechanism to determine whether a container is ready to handle incoming traffic. It plays a mportant role in scenarios where readiness of a service or resource is crucial before allowing the container to receive requests. In this context, the readinessProbe checks the status of an NFS service, ensuring its activation and functionality before proceeding with the creation of the container. This approach enhances the reliability of the containerized application, preventing potential issues that may arise if the required services are not adequately prepared.

You start this deployment by issuing: `kubectl apply -f https://raw.githubusercontent.com/maccu71/projects/master/sonda-readiness-tcp.yml` but probably you don't have configured NFS on provided address/path..

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
Kick it out by issuing:
`kubectl delete -f https://raw.githubusercontent.com/maccu71/projects/master/sonda-readiness-tcp.yml`
