Here you will find 4 small programs designed/aimed at confirming the ability to freely program small applications and scripts in Python. Here they are:

1) stacje.py - downloads a list of radio stations from the net and allows you to select one from the list, starts it and shows the name of the artist and song. This is a really nice app you can start off just from your linux console
2) cwicz.py, which was created to track and backup my running results and display them on a nice graph. This application uses the matplotlib, time, and json modules.
![obraz](https://github.com/maccu71/projects/assets/51779238/4cd59ca3-d49e-435e-a71b-6646fa46218e)
   
4) init-containers-usage - a compressed helm package that illustrates how to use init-containers in Kubernetes cluster. 

![obraz](https://github.com/maccu71/projects/assets/51779238/d982af6a-e8ef-4a85-b30a-4619db6070a1)

To install deployment with service you need to:
1) have working Kubernetes cluster eg. Minikube
<<<<<<< HEAD
2) helm install release-name https://raw.githubusercontent.com/maccu71/projects/master/init-containers-usage-1.0.0.tgz
3) helm install my-release init-containers-usage-1.0.0.tgz
4) see the picture on localhost port:  kubectl get service my-release -o jsonpath='{.spec.ports[*].nodePort}'|jq  
OR use: minikube service my-release
=======
2) #helm add repo repo-name https://github.com/maccu71/projects/init-containers-usage-1.0.0.tgz
4)  git pull https://github.com/maccu71/projects/
4) #helm repo update 
5) helm install depoyment-name init-containers-usage-1.0.0.tgz
>>>>>>> 30b620666e6193dc8e6daf136a024c6fd4ac108f

