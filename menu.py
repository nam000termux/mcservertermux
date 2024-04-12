import os
from threading import Thread
import requests
import time
import shutil
import sys
import netifaces

try:
  prefix=os.getenv("PREFIX")
  home=os.getenv("HOME")
  if not os.path.exists(prefix+"/tmp/mcsv.status"):
    try:
      open(prefix+"/tmp/mcsv.status", "x")
    except:
      pass
  def installsv():
    os.system(f"python {home}/install.py -noupdate")
  if not os.path.exists("/sdcard/mcsv"):
    installsv()
  def killtask():
    os.system("pkill java >/dev/null 2>&1")
    os.system("pkill tmux >/dev/null 2>&1")
  def onserver():
    open(prefix+"/tmp/mcsv.status", "w").write("on")
    global serverdabat
    serverdabat=True
  def offserver():
    killtask()
    open(prefix+"/tmp/mcsv.status", "w").write("off")
    global serverdabat
    serverdabat=False

  os.system("clear")

  if open(prefix+"/tmp/mcsv.status", "r").read().lower() == "on":
    onserver()
  else:
    offserver()
  worldname=["world"]
  once = True

  if ("-start" in sys.argv) and (not serverdabat):
      open(f"{home}/.tmux.conf", "w").write('set -g status off')
      os.chdir("/sdcard/mcsv")
      try:
        open("eula.txt", "x")
      except:
        pass
      if not "eula=true" in open("eula.txt", "r").read():
        match input("""Bạn có đồng ý eula của minecraft ? (https://account.mojang.com/documents/minecraft_eula) [y/n] [y]: """).lower():
          case "n":
            exit()
          case other:
            open("eula.txt", "w").write("eula=true")
      os.system('tmux new-session -d -s minecraft "bash /sdcard/mcsv/start.sh"')
      onserver()
  elif ("-stop" in sys.argv) and serverdabat:
    offserver()
  class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

  while True:
    print(f"{style.WHITE}Minecraft Server menu by fb.com/nam000creeda")
    meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
    memtotal = round(meminfo['MemTotal']/1000)
    memfree = round(meminfo['MemFree']/1000)
    swaptotal = round(meminfo['SwapTotal']/1000)
    swapfree = round(meminfo['SwapFree']/1000)
    try:
      for _ in open("/sdcard/mcsv/server.properties", "r").read().split("\n"):
        if "server-port=" in _:
          serverport=_.split("=")[1]
          break
    except:
      serverport="25565"
    print(f"""{style.RED}RAM: {memtotal} MB | Free: {memfree} MB
Swap: {swaptotal} MB | Free: {swapfree} MB
    """)
    try:
      ipgateway=netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
    except:
      ipgateway="localhost"

    if open(prefix+"/tmp/mcsv.status", "r").read().lower() == "on":
      serverdabat=True
    else:
      serverdabat=False

    if serverdabat:
      tinhtrangserver = f"{style.GREEN}🟢Đang bật\n{style.CYAN}Cách mở console: vuốt trái sang phải  chọn New Session và nhập lệnh console"
    else:
      tinhtrangserver = f"{style.RED}🔴Server chưa bật{style.CYAN}"
    if serverport == "25565":
      print(f"""{style.CYAN}Tình trạng server: {tinhtrangserver}
IP offline: {ipgateway} hoặc 127.0.0.1
  """)
    else:
      print(f"""{style.CYAN}Tình trạng server: {tinhtrangserver}
IP wifi: {ipgateway}:{serverport} hoặc 127.0.0.1:{serverport}
  """)
    print(f"""{style.YELLOW}0. FAQ
1. Bật/Tắt server
2. Tùy chỉnh server.properties
3. Thế giới
4. Đổi phiên bản và loại server
5. Force stop (Dùng khi server đã tắt nhưng vẫn còn chạy)
6. Reload menu
7. Tùy chỉnh JVM
q. Thoát khỏi menu
""")
    choose=input(f"{style.CYAN}Lựa chọn: ")
    os.system("clear")
    match choose:
      case "0":
        print("""1. Cài plugin ngoài?
A: Tải plugin vào file mcsv/plugins""")
        input(f"{style.YELLOW}[Ấn enter để quay lại menu]")
        os.system("clear")
      case "1":
        if not serverdabat:
          open(f"{home}/.tmux.conf", "w").write('set -g status off')

          os.chdir("/sdcard/mcsv")
          try:
            open("eula.txt", "x")
          except:
            pass
          if not "eula=true" in open("eula.txt", "r").read():
            match input("""Bạn có đồng ý eula của minecraft ? (https://account.mojang.com/documents/minecraft_eula) [y/n] [y]: """).lower():
              case "n":
                exit()
              case other:
                open("eula.txt", "w").write("eula=true")
          os.system('tmux new-session -d -s minecraft "bash /sdcard/mcsv/start.sh"')
          onserver()
          input(f"""Chạy server thành công!
{style.YELLOW}[Ấn enter để trở lại menu]""")
          os.system("clear")
        else:
          os.system('tmux send -t minecraft "stop" ENTER')
          open(prefix+"/tmp/mcsv.status", "w").write("off")
          serverdabat=False
          input(f"""Dừng server thành công!
{style.YELLOW}[Ấn enter để trở lại menu]""")
          os.system("clear")
      case "2":
        os.system("nano /sdcard/mcsv/server.properties")
        os.system("clear")
      case "3":
        if serverdabat:
          print("Tắt server trước khi làm điều này!")
          input(f"{style.YELLOW}[Ấn enter để tiếp tục]")
        else:
          print(f"{style.YELLOW}1. Tạo thế giới mới và xóa thế giới cũ")
          while True:
            match input(f"{style.CYAN}Lựa chọn: "):
              case "1":
                if input("Bạn có chắc chắn muốn xóa thế giới ? [y/n] [n]: ").lower() in ["y", "yes"]:
                  for __ in open("/sdcard/mcsv/server.properties").read().split("\n"):
                    if ("level-name=" in __) and (not __.split("=")[1] in worldname):
                      worldname=__.split("=")[1]
                  try:
                    shutil.rmtree(f"/sdcard/mcsv/{worldname}", ignore_errors=True)
                    shutil.rmtree(f"/sdcard/mcsv/{worldname}_nether", ignore_errors=True)
                    shutil.rmtree(f"/sdcard/mcsv/{worldname}_the_end", ignore_errors=True)
                  except:
                    pass
                os.system("clear")
                break
      case "4":
        if serverdabat:
          print("Tắt server trước khi làm điều này!")
          input(f"{style.YELLOW}[Ấn enter để tiếp tục]")
        else:
          installsv()
      case "5":
        if input("Server có thể bị lỗi file thế giới bạn có muốn tiếp tục?[y/n] [n]: ") in ["yes", "y"]:
          offserver()
        os.system("clear")
      case "6":
        os.system("clear")
        continue
      case "7":
        os.system("nano /sdcard/mcsv/jvm.txt")
        os.system("clear")
      case "q":
        if serverdabat:
          while True:
            print("""1. Tắt menu và force stop server
2. Tắt menu và giữ server
q. Quay lại menu
    """)
            match input("Lựa chọn: "):
              case "1":
                if input("Server có thể bị lỗi file thế giới bạn có muốn tiếp tục?[y/n] [n]: ") in ["yes", "y"]:
                  offserver()
                os.system("clear")
                exit()
              case "2":
                exit()
              case "q":
                break
              case other:
                print("Lựa chọn không hợp lệ!")
                input(f"{style.YELLOW}Ấn enter để trở lại")
        else:
          offserver()
          os.system("clear")
          exit()


      case other:
        os.system("clear")
        print("Lựa chọn không hợp lệ!")
        input(f"{style.YELLOW}[Ấn enter để trở lại]")
        os.system("clear")

except KeyboardInterrupt:
  os.system("clear")
  offserver()
