import asyncio
from js import document

async def stop_watch(*kargs):
    document.getElementById("btn1").innerHTML = 'Get Set'
    document.getElementById("btn1").className = "btn btn-warning"

    
    for i in range(1,4):
        pyscript.write('time', i)
        await asyncio.sleep(1)

    document.getElementById("btn1").innerHTML = 'Running'
    document.getElementById("btn1").className = "btn btn-secondary"
    document.getElementById("btn1").setAttribute("disabled", True)
    msecond = 0
    second = 0    
    minute = 0    
    hours = 0

    while(True):       
            #print(f'{hours:02} : {minute:02} : {second:02} : {nsecond:02}')     
            await asyncio.sleep(1/1000)    
            msecond+=1    
            if msecond == 99:
                msecond = 0
                second +=1             
            if second == 60:    
                second = 0    
                minute+=1    
            if minute == 60:    
                minute = 0    
                hours+=1
            #print(f'{hours:02} : {minute:02} : {second:02} : {msecond:02}')
            timestamp = f'{hours:02} : {minute:02} : {second:02} : {msecond:02}'
            pyscript.write('time', timestamp)
        
        