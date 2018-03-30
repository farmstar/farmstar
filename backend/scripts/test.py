import com
import fs_serial
import asyncio

def getPort():
    serialport = ["COM5"]
    comport = com.Ports(serialport).valid[0]
    print(comport)
    return(comport)


async def main():
    global comport
    data = loop.create_task(fs_serial.stream(comport).line)
    return data


if __name__ == "__main__":
    print("Getting comport")
    global comport
    comport = getPort()
    try:
        print("Initializing loop")
        loop = asyncio.get_event_loop()
        loop.set_debug(1)
        print("Run until complete")
        line = loop.run_until_complete(main())
        print(line.result())
    except:
        pass
    finally:
        loop.close()
