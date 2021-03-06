import threading
import paho.mqtt.client as mqtt
import time
class SDK(threading.Thread):
    #SDK 1.2 直接用一个Key连接
    def __init__(self,host,port,key,on_message):
        super(SDK, self).__init__()
        self.host=host
        self.port=port
        self.key=key
        self.client = mqtt.Client(self.key.split("-")[2])
        self.client.username_pw_set(self.key.split("-")[2],self.key.split("-")[2])
        self.client.on_message=on_message
        self.client.on_connect=self.on_connect
        self.client.on_disconnect=self.on_disconnect
    def run(self):
        self.client.connect(self.host, self.port, 60)
        self.client.loop_forever()
    def publish(self,data):
        self.client.publish("IN/DEVICE/"+self.key.split("-")[0]+"/"+self.key.split("-")[1]+"/"+self.key.split("-")[2], str(data))
    def on_disconnect(self,a,b,c):
        print("已断开连接,状态码:",c)
    def on_connect(self,c, userdata, flags, rc):
        if rc==0:
            self.client.subscribe("OUT/DEVICE/"+self.key.split("-")[0]+"/"+self.key.split("-")[1]+"/"+self.key.split("-")[2])
            print("连接成功!")
        elif rc==1:
            print("连接失败!MQTT协议错误!")
            self.client.disconnect()
            exit(1)
        elif rc==2:
            print("连接失败!非法客户端标识!")
            self.client.disconnect()
            exit(1)
        elif rc==3:
            print("连接失败!服务器访问失败!")
            self.client.disconnect()
        elif rc==4:
            print("连接失败!账户或者密码错误!")
            self.client.disconnect()
            exit(1)
        elif rc==5:
            print("连接失败!认证失败!")
            self.client.disconnect()
            exit(1)
        else :
            self.client.disconnect()
            exit(1)


def on_message(client, userdata, msg):
    print("Received Data:",msg.payload)
if __name__=="__main__":
    sdk= SDK("localhost",1883,"1527344369841-1527344393672-1527344358402",on_message)
    sdk.start()
    #数据上传
    while 1:
        time.sleep(10)
        sdk.publish(data={"k":"2"})
