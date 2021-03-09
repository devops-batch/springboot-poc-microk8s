pipeline {
    agent any
    stages {
        stage('list repo contents and working directory') {
            steps {
                script {
                    sh "ls"
                    sh "pwd"
                    sh "whoami"
                }
            }
        }
        stage('create build') {
            steps {
                script {
                    sh "./gradlew clean build"
                }
            }
        }
        stage('list the created build file') {
            steps {
                script {
                    sh "ls build/libs/"
                }
            }
        }
        stage('Remove old jar from DOCKER') {
            steps {
                script {
                    sh "sudo rm DOCKER/spring-boot-with-prometheus-0.1.0.jar"
                }
            }
        }
        stage('copy jar to DOCKER') {
            steps {
                script {
                    sh "sudo cp build/libs/spring-boot-with-prometheus-0.1.0.jar DOCKER/"
                }
            }
        }
        stage('building docker image') {
            steps {
                script {
                    sh "cd DOCKER; sudo docker build -t genpactpoc/microk8s-kubernetes-poc:v_${BUILD_NUMBER} ."
                }
            }
        }
        stage('dcoker push') {
            steps {
                script {
                    sh "sudo docker push genpactpoc/microk8s-kubernetes-poc:v_${BUILD_NUMBER}"
                }
            }
        }
        stage('deploying on microk8s') {
            steps {
                script {
                    sh "sudo microk8s.helm3 upgrade --install microk8s --set image.tag=v_${BUILD_NUMBER} /home/ubuntu/kubernetes-poc/"
                    sh "sudo microk8s.kubectl rollout status deployment.apps/microk8s-kubernetes-poc"
                    sh "sudo docker images > unused_images_cid"
                }
            }
        }
        stage ('remove images from build server') {
            steps {
                script {
                    try {
                        sh "sudo docker images -a -q > images_cid; sudo docker rmi `cat images_cid`"
                    } catch (err) {
                        echo err.getMessage()
                    }
                }
                echo currentBuild.result
            }
        }
        stage('port forwarding') {
            steps {
                script {
                     try {
                         sh "kill \$(netstat -ntpl | grep kubectl | awk '{print \$7}' | cut -d / -f 1)"
                        sh "BUILD_ID=dontKillMe nohup microk8s.kubectl port-forward svc/microk8s-kubernetes-poc --address 0.0.0.0 9090:8080 &"
                    } catch (err) {
                        echo err.getMessage()
                    }
                    
                }
            }
        }
        // stage('remove unused images') {
        //     steps {
        //         script {
        //             try {
        //                 sh "sudo docker rmi `cat unused_images_cid`"
        //             } catch (err) {
        //                 echo err.getMessage()
        //             }
        //         }
        //         echo currentBuild.result
        //     }
        // }
    }
}
