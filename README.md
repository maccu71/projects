Here you will find 4 small programs designed/aimed at confirming the ability to freely program small applications and scripts in Python. Here they are:

1) stacje.py - downloads a list of radio stations from the net and allows you to select one from the list, starts it and shows the name of the artist and song. This is a really nice app you can start off just from your linux console.

![obraz](https://github.com/maccu71/projects/assets/51779238/ed8fc9dc-b2ab-41fe-a0d5-b0b1d88a57f6)


2) cwicz.py, which was created to track and backup my running results and display them on a nice graph. This application uses the matplotlib, time, and json modules.
![obraz](https://github.com/maccu71/projects/assets/51779238/4cd59ca3-d49e-435e-a71b-6646fa46218e)
   
3) init-containers-usage - a compressed helm package that illustrates how to use init-containers in Kubernetes cluster. 

![obraz](https://github.com/maccu71/projects/assets/51779238/d982af6a-e8ef-4a85-b30a-4619db6070a1)

To install deployment with service you need to:
1) have working Kubernetes cluster eg. Minikube and Helm installed
2) helm install release-name https://raw.githubusercontent.com/maccu71/projects/master/init-containers-usage-1.0.0.tgz
3) see the picture on localhost port:  kubectl get service my-release -o jsonpath='{.spec.ports[*].nodePort}'|jq  
OR use: minikube service my-release

Init containers in Kubernetes are lightweight, transient containers that run and complete before the main application containers start. They are designed to perform initialization tasks, setup, or any necessary preparations before the main application containers in a pod begin running.

Key points about init containers:

- Initialization Tasks: Init containers are commonly used to perform tasks such as fetching necessary resources, setting up configurations, or waiting for external services to be ready.

- Sequential Execution: Init containers in a pod are executed in order, one after the other. Each init container must complete successfully before the next one starts.

- Separation of Concerns: They allow for the separation of concerns between the initialization process and the main application logic. This can be particularly useful for scenarios where dependencies need to be in place before the main application starts.

- Transient Nature: Once an init container completes its task, it exits. It doesn't run alongside the main application containers during the pod's lifecycle.

In this example, we could use a ConfigMap with a Bash script (what would be the proper way of handling more complicated Bash scripts), but the example is intended to demonstrate the behavior of consecutive init containers."

This version clarifies the potential use of a ConfigMap with a Bash script for more complex scenarios while emphasizing the primary purpose of the example, which is to showcase the behavior of sequential init containers
