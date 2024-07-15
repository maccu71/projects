**Here are some projects related to my interests, including:**
<br/>

**1) Kubernetes - examples:**
- memory-restriction.yml - Explores the concept of resource allocation and memory restriction in K8S
- cpu-restriction.yml - a manifest that serves as a practical demonstration of CPU restrictions implemented both at the deployment specification and the namespace quota level in Kubernetes
- diving into the particularies of Quality of Service - QoS 
- init-containers-usage - a helm package that illustrates the oncept of init-containers in Kubernetes cluster
- cleaner.yml - kubernetes manifest intended to clean unnecessary resources from kubernetes cluster (use with caution)
- sonda-readiness-tcp.yml - A Kubernetes manifest showcasing the capabilities of a readinessProbe, a powerful feature ensuring the operational readiness of containers.
- `rollout-daemonset.yml` - Rolling updates in DaemonSet component in Kubernetes
- `rollout-statefulset.yml` - Diving into StatefulSet update different strategies and its complexities
- allowing and bloking access by network policies in Kubernetes

**2) Ansible - examples:**
- `block` directive in Ansible - usage
-  Understanding different strategies in Ansible
- `run_once` directive: Are You Sure It Runs Only Once?
- differences between `strategy: host_pinned` and `serial:`


**3) Python - examples:**
- stacje.py - an application written in Python 3 that searches for available radio stations, allows you to select one from the list, starts it, and shows the name of the artist and song.
- cwicz.py - a Python program created to track and backup my running results and display them on a nice graph, this application utilizes various Python modules.

**I have done much to ensure that the examples collected here work and do not have errors. 
Anyway, let me know if you spot any error or a room for improvemment here, please. I would be happy to know about it!**

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

<br/> 

You might want to kick out all resources by: `kubectl delete -f https://raw.githubusercontent.com/maccu71/projects/master/cpu-restriction.yml` or simply: `kubectl delete --all -n new` but let's dive into the particularies of `Quality of Service - QoS` within our deployed pods, tightly linked with mentioned CPU and memory restrictions.

<br/><br/>
**diving into the particularies of Quality of Service - QoS**

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

**`init-containers-usage` - a helm package that illustrates the concept of init-containers in Kubernetes cluster** 

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

<br/><br/> 

**`rollout-daemonset.yml` - Rolling updates in DaemonSets component in Kubernetes**

There are two possible update options here - `RollingUpdate` and `OnDelete`.
But let's recall the basic characteristics of DaemonSets firstly.

On every available node, there is only ONE instance. Nevetheless we can use a node selector to run it on specific nodes by labeling the nodes accordingly. This is often simpler than using node affinity, which requires more configuration.
One instance, and only ONE instance, per node, capisce?

Where can we use this setup?

They are particularly useful when you want to run specific services on each node (or specified) in the cluster, like:
- Log Collection: Running log collection agents such as Fluentd or Logstash on each node to gather logs.
- Monitoring: Deploying monitoring agents like Prometheus Node Exporter or Datadog Agent to collect metrics from each node.
- Security: Running security agents that need to monitor and enforce security policies across all nodes.

DaemonSets ensure that certain services are always running on all nodes (or a subset of them) and that new Pods are automatically created when new nodes are added to the cluster. They support rolling updates, allowing you to update the Pods managed by the DaemonSet without downtime.

`Rolling updates` in DaemonSets are like substituting players in a soccer match! You decide how many players to substitute (or rather how many should stay on the field through `maxUnavailable`), and only when one player leaves the field, another can enter. Isn't that a great analogy?

Moreover, with the `minReadySeconds` option, you can check if the player on the field is ready to take action before substituting the next one! Fun, right?

```
spec:
  minReadySeconds: 10
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
```
```
spec:
  minReadySeconds: 10
  updateStrategy:
    type: OnDelete
```
So, just like in a soccer game, you ensure that your team (Pods) is always performing at its best, and only make changes when you're sure the new player is ready.Let's start DaemonSet on 3 nodes now!

Having 2+ nodes start the deployment by issuing: https://raw.githubusercontent.com/maccu71/projects/master/rollout-daemonset.yml

```
$ kubectl get nodes
NAME         STATUS   ROLES           			AGE    VERSION
node-1       Ready    control-plane,master  10d   v1.28.3
node-2   		 Ready    <none>          			10d   v1.28.3
node-3   		 Ready    <none>          			9d 	  v1.28.3
```
```
$ cat rollout-daemonset.yml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  labels:
    app: as
  name: as
spec:
  selector:
    matchLabels:
      app: as
  updateStrategy:
    type: RollingUpdate  ## other option - OnDelete
    rollingUpdate:
      maxUnavailable: 1  ## speaks for itself
  minReadySeconds: 20    ## optional; wait 20 sec to be sure the pod works well
  template:
    metadata:
      labels:
        app: as
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
          - containerPort: 80
```
Let's change containerPort to some other, let's say 8080 forcing kubernetes to rollout and see what happens..
```
$ kubectl get ds --watch
NAME   DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
as     3         3         3       3            3           <none>          81m
as     3         3         3       3            3           <none>          82m
as     3         3         3       0            3           <none>          82m
as     3         3         2       1            2           <none>          83m
as     3         3         3       1            2           <none>          83m
as     3         3         3       1            3           <none>          83m
as     3         3         2       2            2           <none>          83m
as     3         3         3       2            2           <none>          83m
as     3         3         3       2            3           <none>          83m
as     3         3         2       3            2           <none>          84m
as     3         3         3       3            2           <none>          84m
as     3         3         3       3            3           <none>          84m
```
We can see that there is at least 2 nodes avaliable and ready - according to  'maxUnavailable: 1' option.
```
$ kubectl get pod --watch -o wide
NAME       READY   STATUS    					 RESTARTS   AGE   IP           NODE     NOMINATED NODE   READINESS GATES
as-dqpsr   1/1     Running   					 0          77m   10.244.0.4   node-1   <none>           <none>
as-fdttt   1/1     Running   					 0          77m   10.244.2.3   node-3   <none>           <none>
as-gz9pl   1/1     Running   					 0          76m   10.244.1.3   node-2   <none>           <none>
as-fdttt   1/1     Terminating   			 0          77m   10.244.2.3   node-3   <none>           <none>
as-fdttt   0/1     Terminating   			 0          78m   <none>       node-3   <none>           <none>
as-8hd2q   0/1     Pending       			 0          0s    <none>       <none>   <none>           <none>
as-8hd2q   0/1     Pending       			 0          0s    <none>       node-3   <none>           <none>
as-8hd2q   0/1     ContainerCreating   0          0s    <none>       node-3   <none>           <none>
as-8hd2q   1/1     Running             0          1s    10.244.2.4   node-3   <none>           <none>
as-fdttt   0/1     Terminating         0          78m   <none>       node-3   <none>           <none>
as-dqpsr   1/1     Terminating         0          79m   10.244.0.4   node-1   <none>           <none>
as-dqpsr   0/1     Terminating         0          79m   <none>       node-1   <none>           <none>
as-qxqx5   0/1     Pending             0          0s    <none>       <none>   <none>           <none>
as-qxqx5   0/1     Pending             0          0s    <none>       node-1   <none>           <none>
as-qxqx5   0/1     ContainerCreating   0          0s    <none>       node-1   <none>           <none>
as-dqpsr   0/1     Terminating         0          79m   10.244.0.4   node-1   <none>           <none>
as-qxqx5   1/1     Running             0          1s    10.244.0.5   node-1   <none>           <none>
as-gz9pl   1/1     Terminating         0          78m   10.244.1.3   node-2   <none>           <none>
as-gz9pl   0/1     Terminating         0          78m   <none>       node-2   <none>           <none>
as-92cbk   0/1     Pending             0          0s    <none>       <none>   <none>           <none>
as-92cbk   0/1     Pending             0          0s    <none>       node-2   <none>           <none>
as-92cbk   0/1     ContainerCreating   0          0s    <none>       node-2   <none>           <none>
as-gz9pl   0/1     Terminating         0          78m   10.244.1.3   node-2   <none>           <none>
as-92cbk   1/1     Running             0          1s    10.244.1.4   node-2   <none>           <none>
```

We can see the same dance -
- pod is terminating,
- a next one (or more according to maxUnavailable option) is creating and the systems checks its functionality (minReadySeconds: 20)
- the same scheme happens on the next node.

RollingUpdate is the default update strategy in DaemonSet that automatically rolls out changes to Pod instances according to a defined strategy.
When the DaemonSet definition changes (e.g., container image, port), Kubernetes automatically initiates the update process. This involves replacing old Pod instances with new ones, ensuring smooth transition without service disruption (we just need to change manifest and apply it).

If we change 'updateStrategy' to 'OnDelete' we are forced to manual deletion and recreation of Pods after applying changes. The update is not automatically applied to existing Pod instances)

What is the difference between them or Manual or Automatic Update? OnDelete requires user intervention to delete and recreate Pods for updates. RollingUpdate handles this automatically = just change manifest + apply it.
OnDelete can be used for more controlled Pod lifecycle management but increases user management and responsibility = change manifest + apply it + delete pod. 

Final words:
RollingUpdate offers a simpler and more automatic update method. But the choice of strategy depends on specific app. requirements, update policies, and the level of control you want to maintain over the Pod update process in your Kubernetes cluster. 

We can wind up all by issuing: `kubectl delete -f https://raw.githubusercontent.com/maccu71/projects/master/rollout-daemonset.yml` 

Now, a bit about rolling update in StatefulSets, it will be fun!

But, what are those `NOMINATED NODE` and `READINESS GATES` shown on the last output? Let's dive into this topic.

<br/><br/>

**Diving into StatefulSet update different strategies and its complexities**

`StatefulSet` is a Kubernetes component used in stateful applications like databases and anywhere we need to ensure the persistence of data as well as consistent network addressing. It is designed to manage the deployment and scaling of a set of Pods, and provides guarantees about the ordering and uniqueness of these Pods.

StatefulSets are used in situations where each pod needs a unique, stable network identifier.

Persistent storage is required, where each pod must retain its state during its life - across rescheduling and restarts.
Ordered, graceful deployment, scaling, and updates are necessary.

Pods in StatefulSets have predictable names consisting of a base name and sequential numbers starting from 0, which is the most important pod. Each new pod gets the next number in the sequence. For example, if the base name is web, the pods will be named web-0, web-1, web-2, and so on.

Each pod in a StatefulSet can be associated with its own persistent storage using PersistentVolumeClaims (PVCs). These PVCs ensure that even if a pod is rescheduled to a different node, it can still access its persistent data. This feature is crucial for applications like databases, where data consistency and persistence are the most important.

We use headless services with StatefulSets to get predictable and unchanging DNS names for each pod so that we can access them by name. This allows other applications to interact with each pod directly via its stable network identity.

We have 4 replicas of our StatefulSet ,the pods will have DNS names like:
```
state-0.state.default.svc.cluster.local
state-1.state.default.svc.cluster.local
state-2.state.default.svc.cluster.local
state-3.state.default.svc.cluster.local
```
If you want to check it, by using eg. `nslookup` command.

StatefulSets offer the following update strategies:
- `Rolling Update` (Default). In this strategy, the system updates the pods in a sequential order, starting from the last pod (with the highest number) and going down until it finishes with the first pod, number 0. This ensures minimal disruption and allows for careful control over the update process. For example for a StatefulSet with 5 pods (0-4), the update will start with pod-4, then pod-3, and so on, until pod-0.
```
updateStrategy:
  type: RollingUpdate
```

- `Partitioned Rolling Update`. The partition option as a strategy allows us to update only specific pods, leaving some pods with the old configuration. This is useful for controlled rollouts or canary deployments. When a partition value is set, only the pods with a number greater than or equal to the partition value will be updated. For example, if partition: 3 is set, only pods web-3, web-4, and so on will be updated, while web-0 to web-2 remain unchanged.
```
updateStrategy:
  type: RollingUpdate
  rollingUpdate:
    partition: 2
```
- `OnDelete Update` - update strategy offers a high degree of control, making it ideal for scenarios where stability and precision are critical. While it requires more manual effort compared to automated strategies, its benefits in specific situations.
You delete first Pod manually `kubectl delete pod state-0` and wait unless the Kubernetes deploys a new one in place of the old one. Then you repeat the same process on the next and next Pod until the last one.
```
updateStrategy:
  type: OnDelete
```

Now, let's focus on 'partition' style of update and change the manifest by uncommenting two lines from `rollout-stateful-set.yml`:  `rollingUpdate:` and `partition: 2`, changing the image to `nginx:latest` and finally applying changes by issuing `kubectl apply -f rollout-stateful-set.yml`. By doing this we force Kubernetes to update only pods: as-2 and as-3. After a while we can see the result:
```
$ kubectl get pods -o=custom-columns=NAME:metadata.name,IMAGE:spec.containers[0].image,START_TIME:status.startTime
NAME                  IMAGE                    START_TIME
dd-6d7594d974-t9vlw   macosmi/nginxshowip:v1   2024-06-23T18:58:54Z
state-0               nginx:1.14.2             2024-06-23T18:57:47Z
state-1               nginx:1.14.2             2024-06-23T18:57:50Z
state-2               nginx:latest             2024-06-23T19:07:15Z <== different image applied
state-3               nginx:latest             2024-06-23T19:07:13Z <== different image applied
```
```
$ kubectl get pod
NAME                  READY   STATUS    RESTARTS   AGE
state-0               1/1     Running   0          16m
state-1               1/1     Running   0          16m
state-2               1/1     Running   0          6m52s
state-3               1/1     Running   0          6m54s
```
These strategies can be combined with `minReadySeconds`, which ensures that after a pod is updated, it must be in a ready state for a specified number of seconds before proceeding to update the next pod. This adds an additional layer of stability to the rolling update process.

StatefulSets update strategies, including `rolling updates` and `partitioned updates`, offer flexibility and control over the update process, making them ideal for managing stateful applications in Kubernetes.

<br/><br/> 
**allowing and bloking access via network policies in Kubernetes**

`Ingress policy`:
```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: 
  name: restrict
  namespace: default
spec:
  podSelector:
    matchLabels:
      ver: three
  ingress:
  - from: 
    - podSelector:
        matchLabels:
          ver: two
    ports:
    - port: 80
```
```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: egress-1
  namespace: default
spec:
  podSelector:
    matchLabels:
      ver: two
  egress:
  - to:
    - podSelector:
        matchLabels:
          ver: three
    ports:
    - port: 81
      protocol: TCP
    - port: 443
      protocol: TCP
  policyTypes:
  - Egress
```
```
$ kubectl describe networkpolicy egress-1 
Name:         egress-1
Namespace:    default
Created on:   2024-06-24 20:47:03 +0200 CEST
Labels:       <none>
Annotations:  <none>
Spec:
  PodSelector:     ver=two
  Not affecting ingress traffic
  Allowing egress traffic:
    To Port: 81/TCP
    To Port: 443/TCP
    To:
      PodSelector: ver=three
  Policy Types: Egress
```
```
$ kubectl get networkpolicy -n default
NAME       POD-SELECTOR   AGE
egress-1   ver=three      11s
```
```
Name:         restrict
Namespace:    default
Created on:   2024-06-24 21:08:43 +0200 CEST
Labels:       <none>
Annotations:  <none>
Spec:
  PodSelector:     ver=three
  Allowing ingress traffic:
    To Port: 80/TCP
    From:
      PodSelector: ver=two
  Not affecting egress traffic
  Policy Types: Ingress
```
```
  ingress:
  - from: 
    - podSelector:
        matchLabels:
          ver: two
    - podSelector:
        matchLabels:
          run: one
```
<br/><br/>

**`stacje.py` - an application written in Python 3 that searches for available radio stations, allows you to select one from the list, starts it, and shows the name of the artist and song.**

 This is a really nice app that you can launch directly from your Linux console. Start the program in your linux console by issuing: 
`python3 stacje.py` 
or just 
`./stacje.py````

<br/><br/>

**`cwicz.py` - a Python program created to track and backup my running results and display them on a nice graph, this application utilizes various Python modules.**
![obraz](https://github.com/maccu71/projects/assets/51779238/887d3e3c-b59d-4a1c-bac3-c4e738d7160f)

<br/><br/> 


**'block' directive in Ansible - usage:**

Have you ever wondered what the 'block' directive in Ansible is and what its exact purpose is?

Let's clarify and highlight its beneficial role.

There are two main ways we can utilize the 'block' directive:
1) Grouping tasks as a single unit: This helps to apply logic effectively.
2) Handling errors elegantly: This is achieved through the Block-Rescue-Always directives.

For instance, let's say we want to install the Apache server on CentOS nodes. This involves installing the httpd package, copying files, changing config files, copying website code, and finally, restarting the httpd service. While we could include "- when: ansible_distribution == CentOS'" after each task, it would be impractical, making the code unreadable and unprofessional.

Here's where the Block directive comes to the rescue.

A simple example using the block directive (simplified for the purpose):

```
---
- name: example using block
  gather_facts: yes
  hosts: all
  tasks:
    - name: install Apache
      block:
        - name: install package http
          yum:
            name: httpd
            state: latest
        - name: restart service httpd
          service:
            name: httpd
            state: restarted
      when: ansible_distribution == 'CentOS'
```
Here, we don't need to apply the 'when' clause after each task. This allows us to apply logic to our code more efficiently.

By the way, this is not the only way to handle different OS in Ansible playbooks; you can use for example 'group_by' module, for example.

The second important role is applying the 'block' directive to handle errors in playbook, as seen below:
```
---
- name: error handling example
  hosts: all
  tasks:
    - name: error handling block
      block:
        - name: successful task
          debug:
            msg: 'first task OK..'
        - name: intentional error
          command: cat /nothinghere
      rescue:
        - name: actions when task in block encounters an error
          debug:
            msg: 'we encountered an error..'
      always:
        - name: tasks always done
          debug:
            msg: 'a task from the Always block of code'
```
And here are some rules to follow:

- Tasks in the 'block' directive are performed sequentially, unless they fail.
- Tasks in the Rescue directive start only if at least one in the 'block' finished with an error.
- If there are errors in the Rescue block of code, the program jumps to the Always tasks.
- Finally, tasks in the Always block of code are performed independently of the previous 'Block' and 'Rescue' outcomes.

This allows us to apply another layer of logic to our Ansible code. Isn't it beautiful?

This method, combined with a debug strategy, allows us to precisely identify the type of error encountered. We'll delve into 'debug' mode later on.

**Understanding different Ansible Strategies**

In this example, we'll explore and discuss the different strategies available in Ansible.
```
---
- name: applying different strategies
  strategy: host_pinned
  # strategy: free
  # strategy: linear - implicitly default (no need to specify it)
  # strategy: debug
  hosts: all
  tasks:
    - name: first task
      shell: sleep 2
    - name: second task
      shell: sleep 2
```
Ansible offers several strategies for executing tasks in playbooks. You might wonder what these strategies are and how they function. Let's break it down.

To list the available strategies, you can use the following command:
```
$ ansible-doc -t strategy -l
ansible.builtin.debug       Executes tasks in an interactive debug session
ansible.builtin.free        Executes tasks without waiting for all hosts
ansible.builtin.host_pinned Executes tasks on each host without interruption...
ansible.builtin.linear      Executes tasks in a linear fashion
```
Using the -t switch, we can access plugin information in Ansible.

By default, Ansible employs the `'Linear'` strategy (that mean's you need not specify in in your playbook) and tasks are executed sequentially, maintaining order and ensuring dependencies are met across hosts. Let's see how looks like the 'Linear' strategy:

```
$ ansible-playbook strategy.yml -f 1
PLAY [applying different strategies] ********************************************************************************************************

TASK [first task] ***************************************************************************************************************************
changed: [192.168.122.201]
changed: [192.168.122.202]
changed: [192.168.122.203]

TASK [second task] **************************************************************************************************************************
changed: [192.168.122.201]
changed: [192.168.122.202]
changed: [192.168.122.203]
```

While the 'Linear' strategy provides order and predictability, it may slow down execution, especially with a large number of hosts.

The `'Host Pinned'` strategy, on the other hand, executes tasks on each batch of host without interruption. Setting the number of forks to 1 (number of hosts in a batch = 1) ensures sequential execution, revealing the precise task sequence.

Let's uncomment the line with: `#strategy: host_pinned` in strategy.yml and run it. Executing tasks with the 'Host Pinned' strategy gave us the following input:

```
$ ansible-playbook strategy.yml -f 1

PLAY [applying different strategies] ********************************************************************************************************

TASK [first task] ***************************************************************************************************************************
changed: [192.168.122.203]

TASK [second task] **************************************************************************************************************************
changed: [192.168.122.203]

TASK [first task] ***************************************************************************************************************************
changed: [192.168.122.201]

TASK [second task] **************************************************************************************************************************
changed: [192.168.122.201]

TASK [first task] ***************************************************************************************************************************
changed: [192.168.122.202]

TASK [second task] **************************************************************************************************************************
changed: [192.168.122.202]
```

As you have seen - all tasks were performed on one host (or on group of hosts if we didn't specify 'fork' directive or give -f more than one) and to the other, and so on.  

And lastly - executing tasks with the 'Free' strategy:
We need to uncmment the line: 
`# strategy: free`

```
PLAY [applying different strategies] ********************************************************************************************************

TASK [first task] ***************************************************************************************************************************
changed: [192.168.122.203]
changed: [192.168.122.201]
changed: [192.168.122.202]

TASK [second task] **************************************************************************************************************************
changed: [192.168.122.203]
changed: [192.168.122.201]
changed: [192.168.122.202]
```

Lastly, the 'Debug' strategy operates similarly to 'Linear', but with debug information returned. We'll delve into this strategy further in a separate example.

Conclusion: choosing the appropriate strategy depends on factors such as inventory size, task nature, and the desired balance between predictability and speed.

Additionally, we can specify the default strategy using the ANSIBLE_STRATEGY environmental variable or by configuring it in the ansible.cfg file for all playbooks.

**Run-Once Directive in Ansible: Are You Sure It Runs Only Once?**

In this example, I would like to discuss the run_once directive and demonstrate how its behavior might not correspond to its name. Can you believe it?

By default, tasks in Ansible are like a well-organized party—they're run one at a time on a group of hosts (the default number is 5) before moving to the next task. However, this behavior depends on the applied strategy. Just like party planning, the behavior can be modified using special directives, such as serial.

The 'run_once' directive is used when you need or want to run certain task(s) only once. This can be useful for getting the value of some variable or making changes in a configuration. While some situations can be handled by specifying a host in the inventory, this might not always be sufficient and can introduce inconsistencies. It's like telling one friend to bring chips but ending up with five bags of chips and no dip. Awkward!

This is where the run_once directive swoops in to save the day!

```
---
- name: Directive run_once in action
  hosts: all
  gather_facts: no
  #strategy: host_pinned
  #serial: 1
  tasks:
    - name: First task - with run_once
      shell: 'echo this task is with run_once'
      run_once: yes
    - name: Second task - without run_once
      shell: 'echo this task is without run_once'
```
When we run this playbook, we will see the following output:

```
$ ansible-playbook run_once.yml

PLAY [directive run_once in action] ********************************************

TASK [First task - with run_once] **********************************************
changed: [192.168.122.203]

TASK [Second task - without run_once] ******************************************
changed: [192.168.122.203]
changed: [192.168.122.201]

PLAY RECAP *********************************************************************
192.168.122.201            : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.122.203            : ok=2    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

The playbook behaves as expected—the first task, thanks to the run_once directive, was executed only once. Bravo, run_once, you did your job!

Keep in mind that we have only two hosts in our inventory. Let's check it out:

```
$ ansible-inventory --graph 
@all:
  |--@ungrouped:
  |  |--192.168.122.203
  |  |--192.168.122.201
```
Let's spice things up a bit by uncommenting the 'serial: 1' option. This enforces running all tasks on one host and then all tasks on the next, and so on. We use the serial option to specify how many hosts tasks should be executed on before moving to the next set (in other words, we specify how many hosts are in a batch to be executed simultaneously). Setting serial to 1 enforces that all tasks be executed on one host at a time before moving to the next. It's like making sure one friend finishes their karaoke song before the next friend starts—no chaotic duets here!

We use the serial option when we don't want Ansible tasks to be executed at the same time or when we want to narrow down the number of hosts (e.g., to maintain the application’s functionality in a load-balancing scheme).

```
$ ansible-playbook run_once.yml 

PLAY [directive run_once in action] ********************************************

TASK [First task - with run_once] **********************************************
changed: [192.168.122.203]

TASK [Second task - without run_once] ******************************************
changed: [192.168.122.203]

PLAY [directive run_once in action] ********************************************

TASK [First task - with run_once] **********************************************
changed: [192.168.122.201]

TASK [Second task - without run_once] ******************************************
changed: [192.168.122.201]

PLAY RECAP *********************************************************************
192.168.122.201            : ok=2    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.122.203            : ok=2    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Interestingly, we get the same output when we uncomment 'strategy: host_pinned', which enforces tasks to be executed one by one.

How come? Why was the first task labeled with 'run_once: yes' executed on all hosts?

**We must keep in mind that the run_once directive refers to the specified batch of servers, not the entire inventory.** It's like telling a joke to one small group at a party and then realizing you have to repeat it to each new group that joins in.

We also noticed that the 'run_once' directive behaves similarly to the 'strategy: host_pinned' by enforcing running all tasks sequentially but here is lie the cat:
1) `serial: 1` performes all tasks on exactly one host after antother from the inventory
2) `strategy: host_pinned` - performes sequential tasks on a batch of 5 hosts by default or the number specified in `fork` directive. Thus: `strategy: host_pinned` and `-f 1` during playbook execution effectively equals: `serial 1`
