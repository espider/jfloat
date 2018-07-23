# Jfloat
jfloat is the tool that help you troubleshoot the running JVM(1.6-1.8) on linux.

## Installation

```shell
git clone https://github.com/espider/jfloat
```

## Used

* find jvm PID by `jps` or `ps`
* run jfloat with the -p &lt;pid&gt; and other options. 

```
./jfloat.py -h

welcome jfloat.
usage: jfloat.py [-h] -p PID [-i] [-s] [-m] [-g GCSTAT] [-o OBJECT]

optional arguments:
  -h, --help            show this help message and exit
  -p PID, --pid PID     PID for java process
  -i, --info            dump base info for java process
  -s, --stack           find which threads that make high CPU
  -m, --map             dump the heap info for JVM
  -g GCSTAT, --gcstat GCSTAT
                        get statistics of the garbage collected heap
  -o OBJECT, --object OBJECT
                        get object count change by seconds
```

* use the -i option can show JVM base information 
* use the -s option can show top 10 threads that make high CPU and these call stack.
* use the -m option can show the JVM Heap Config information.
* use the -g option with integer second get statistics of the garbage collected heap.
* use the -o option with integer second get top 10 increase and decrease objects.

## Output Demo

```
# ./jfloat.py -p 19710 -i

welcome jfloat.
pid 19710
java.runtime.version = 1.8.0_131-b11
os.name = Linux
file.encoding = UTF-8
java.specification.version = 1.8
user.name = root
java.class.path = .
java.vm.specification.version = 1.8
sun.arch.data.model = 64
sun.java.command = highCPU
java.home = /opt/java/jre
java.version = 1.8.0_131
file.separator = /
sun.cpu.endian = little
VM Flags:
Non-default VM flags: -XX:CICompilerCount=4 -XX:InitialHeapSize=130023424 -XX:MaxHeapSize=2061500416 -XX:MaxNewSize=686817280 -XX:MinHeapDeltaBytes=524288 -XX:NewSize=42991616 -XX:OldSize=87031808 -XX:+UseCompressedClassPointers -XX:+UseCompressedOops -XX:+UseParallelGC
``` 

* base infomation by pid.

```
# ./jfloat.py -p 19710 -s

welcome jfloat.
pid 19710
--------------------------------------------------
nid:[0x4d13] CPU:[101.1%]
"pool-1-thread-2" #11 prio=5 os_prio=0 tid=0x00007f24c8101000 nid=0x4d13 runnable [0x00007f24b17d7000]
   java.lang.Thread.State: RUNNABLE
        at highCPU$Task.calculate(highCPU.java:27)
        at highCPU$Task.run(highCPU.java:21)
        at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)
        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)
        at java.lang.Thread.run(Thread.java:748)
   Locked ownable synchronizers:
        - <0x00000000d715e400> (a java.util.concurrent.ThreadPoolExecutor$Worker)
--------------------------------------------------
nid:[0x4d12] CPU:[99.2%]
"pool-1-thread-1" #10 prio=5 os_prio=0 tid=0x00007f24c80ff000 nid=0x4d12 runnable [0x00007f24b18d8000]
   java.lang.Thread.State: RUNNABLE
        at highCPU$Task.calculate(highCPU.java:27)
        at highCPU$Task.run(highCPU.java:21)
        at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)
        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)
        at java.lang.Thread.run(Thread.java:748)
   Locked ownable synchronizers:
        - <0x00000000d715e0a0> (a java.util.concurrent.ThreadPoolExecutor$Worker)
```

* find top 10 threads that make high CPU and these call stack.

```
# ./jfloat.py -p 20010 -m

welcome jfloat.
pid 20010
--------------------------------------------------
JVM Config Info
NewSize: 41.0M
NewRatio: 2
SurvivorRatio: 8
OldSize: 83.0M
MinHeapFreeRatio: 0
MaxHeapFreeRatio: 100
MaxHeapSize: 6.0G
MetaspaceSize: 20.8M
```

* JVM Heap Config information

```
# ./jfloat.py -p 20010 -g 10

welcome jfloat.
pid 20010
    EC      EP   SC0/1   SP0/1      OC      OP      MC      MP     YGC     FGC     GCT
------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------
 18.0M   87.6%   61.5M   77.9%  235.5M   76.8%    4.8M   80.7%       -       -       -
 18.0M    4.1%   34.0M   10.0%  295.5M   79.7%    4.8M   80.7%      +1      +1    56ms
 18.0M   25.1%   34.0M   10.0%  295.5M   79.7%    4.8M   80.7%       -       -       -
 18.0M   48.1%   34.0M   10.0%  295.5M   79.7%    4.8M   80.7%       -       -       -
 18.0M   69.0%   34.0M   10.0%  295.5M   79.7%    4.8M   80.7%       -       -       -
 18.0M   90.0%   34.0M   10.0%  295.5M   79.7%    4.8M   80.7%       -       -       -
 16.5M   12.2%   61.5M   26.4%  295.5M   80.6%    4.8M   80.7%      +1       -     6ms
 16.5M   30.6%   61.5M   26.4%  295.5M   80.6%    4.8M   80.7%       -       -       -
 16.5M   53.0%   61.5M   26.4%  295.5M   80.6%    4.8M   80.7%       -       -       -
 16.5M   71.4%   61.5M   26.4%  295.5M   80.6%    4.8M   80.7%       -       -       -
```

* show GC info by 10s,1 times per second. 

```
# ./jfloat.py -p 20010 -o 10

welcome jfloat.
pid 20010
total increase object count :1528
--------------------------------------------------
increase top 10 object:
   +count    current  class
---------  ---------  ---------
     2889      85253  [B
     2889      84858  temp
--------------------------------------------------
decrease top 10 object:
   -count    current  class
---------  ---------  ---------
    -1183       1887  [Ljava.lang.String;
     -819       4505  [C
     -519        643  [I
     -182        258  java.nio.HeapCharBuffer
     -182        259  java.text.DecimalFormatSymbols
     -182        258  java.util.Date
     -182        259  java.text.DateFormatSymbols
      -91        129  sun.util.calendar.Gregorian$Date
      -91        129  java.text.SimpleDateFormat
      -91        134  sun.util.calendar.ZoneInfo
--------------------------------------------------
```

* show increase and decrease objects by 10s.

## License
Jfloat is BSD-licensed. 

