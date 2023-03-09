#!/bin/bash
serverName="app.py"
echo "serverName=${serverName}"
#ps -aux | grep ${serverName}
#get server pid number 
pid=$(ps -aux | grep ${serverName} |grep "python3" | awk '{print $2}')
echo "serverPid=${pid}"
#kill server process
if [ -n ${pid} ];then
        echo "kill serverPid=${pid}"
        kill -9 ${pid}
esle
        echo "${serverName} is null,can not kill serverPid=${pid}"
fi
#restart server process
nohup python3 app.py &
tail -f nohup.out
