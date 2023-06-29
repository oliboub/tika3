# <span style="color:orange"> Support on behaviour using tika</span>
Note: these hints are coming when using ubuntu. Not sure about mac or windows


## <span style="color:blue">tika</span>
**at the first start, java is not initiated.**<br>
You can encounter this message (on by parallel process):<br>
<u>Date - Hour  [MainThread  ] [WARNI]  Failed to see startup log message; retrying...</u><br>
the best is to stop the script, and relaunch it. otherwise, some files might be not treated.<br>

## <span style="color:blue">Parallelization.</span>
In case of too much parrallelisation, the server will get retrying message. Reduce parrallel parameter in global_variables.py.<br>
Monitor the usage of your CPU, if you reach always 100% , reduce the parallelization.<br>
The disk migth be also the slowdown point. check the i/os<br>
**Parallelization need to be tuned. The performance, wil increase by parrallelizing, but migth decrease if parallelization is to high. Tune your system to find the correct parrallelization factor.**<br>


## <span style="color:blue">Tesseract</span>
Tika is using tesseract process. when cancelling the python script (ctrl-C or control-D), some tesseract processes are still running until the end of treatement, and it can takes few seconds.<br>
If you relaunch immediatly the python script, you migth get a wrong list of remaining files. It is due that the update is still running util th end of all completion, despite the stop of th escript.
Be patient, and wait a litle bit.<br>
If you see that tesseracts proces are two long to kill after a cancell of process, you might have too many parallel proces. Reduce the parameter.<br>

## <span style="color:blue">Java (only Linux)</span>
Java is using a lot of memory, and more you treat documents, more the jvm will use memory.<br>
Usually there is a garbage collector to clean java memory. But at the end of the script, I have added a java killer.<br>
Be carefull, it is not linked to the java of th eprgrtam yet. you could kill another java stack, so if some problems occurs on other java program, remove the call of the java kill.