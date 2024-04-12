import requests, subprocess, os, sys

prefix=os.getenv("PREFIX")
home=os.getenv("HOME")
os.system("clear")
while True:
  try:
    open("/sdcard/testtermuxstorage.txt", "w").write("hi")
    break
  except IOError:
    os.system("termux-setup-storage"),
    input("Chọn đồng ý và ấn nhập enter!")
    os.system("clear")

try:
  os.remove("/sdcard/testtermuxstorage.txt")
except:
  pass

if not os.path.exists(prefix+'/bin/java'):
  allversionjava=subprocess.check_output(["pkg", "list-all", "*jdk*"]).decode("utf-8")+"\n"+subprocess.check_output(["pkg", "list-all", "*jre*"]).decode("utf-8")
  os.system("clear")
  allversionjava_=[]

  u=1
  for _ in allversionjava.split("\n"):
    version=_.split("/")[0]
    if "jdk" in version or "jre" in version:
      print(str(u) + ".", version)
      allversionjava_.append(version)
      u+=1
  print("q. Thoát")
  while True:
    try:
      loaijava=input("Vui lòng chọn loại java: ")
      if loaijava=="q":
        os.system("clear")
        exit()
      tenjava=allversionjava_[int(loaijava)-1]
      break
    except ValueError:
      continue
os.system("clear")
while True:
  print("""1. Paper
2. Vanilla
3. Chọn file jar từ url
q. Thoát khỏi menu
""")
  loaiserver=input("Vui lòng chọn loại minecraft server: ")
  os.system("clear")
  match loaiserver.lower():
    case "1":
      allversion=requests.get("https://api.papermc.io/v2/projects/paper").json()["versions"][::-1]

      u=1
      for i in allversion:
        print(str(u) + ".", i)
        u+=1
      print("q. Trở lại")
      while True:
        input1 = input("Vui lòng chọn phiên bản minecraft server: ")
        try:
         version=allversion[int(input1)-1]
         quit=False
         break
        except:
          if input1.lower() == "q":
            quit=True
            os.system("clear")
            break
          else:
            print("Lựa chọn không hợp lệ!")
      if not quit:
        build = requests.get("http://api.papermc.io/v2/projects/paper/versions/" + version).json()["builds"][-1]

        namefile = requests.get(f"http://api.papermc.io/v2/projects/paper/versions/{version}/builds/{build}").json()["downloads"]["application"]["name"]
        os.system("clear")
        print(f"Đang tải paper {version}\nCó thể mất một chút thời gian!")
        serverresponse = requests.get(f"http://api.papermc.io/v2/projects/paper/versions/{version}/builds/{build}/downloads/{namefile}")


        open("/sdcard/mcsv/server.jar", "wb").write(serverresponse.content)
        break
    case "2":
      vanillalist = requests.get("https://raw.githubusercontent.com/nam000termux/mcservertermux/main/vanilla/vanilla.json").json()
      i = 1
      for _ in vanillalist["version"]:
        print(str(i)+".", _)
        i+=1
      k=input("Chọn phiên bản: ")
      try:
        k=vanillalist["version"][int(k)-1]
        os.system("clear")
        print(f"Đang tải vanilla {k}\nCó thể mất một chút thời gian!")
        serverresponse = requests.get(vanillalist[k])
        open("/sdcard/mcsv/server.jar", "wb").write(serverresponse.content)
        break
      except:
        if k == "q":
          quit=True
          os.system("clear")
    case "3":
      url=input("Nhập link jar file: ")
      os.system("clear")
      print(f"Đang tải custom jar\nCó thể mất một chút thời gian!")
      serverresponse = requests.get(str(url))
      open("/sdcard/mcsv/server.jar", "wb").write(serverresponse.content)
    case "q":
      exit()
    case other:
      os.system("clear")
if not os.path.exists(prefix+'/bin/java'):
  os.system("clear")
  print(f"Đang cài đặt {tenjava}")
  os.system("pkg install -y " + tenjava + " >/dev/null 2>/dev/null")
if not os.path.exists("/sdcard/mcsv"):
  os.makedirs("/sdcard/mcsv")
if not "-noupdate" in sys.argv:
  open(home+"/.termux/termux.properties", "a").write("\nallow-external-apps = true")
  os.system("termux-open /sdcard/ZArchiverPro.apk")
  serverresponse = requests.get("https://raw.githubusercontent.com/nam000termux/mcservertermux/main/mcsv")
  open(prefix + "/bin/mcsv", "wb").write(serverresponse.content)
  os.system(f"chmod +x {prefix}/bin/mcsv")
  serverresponse = requests.get("https://raw.githubusercontent.com/nam000termux/mcservertermux/main/console")
  open(prefix + "/bin/console", "wb").write(serverresponse.content)
  os.system(f"chmod +x {prefix}/bin/console")
  serverresponse = requests.get("https://raw.githubusercontent.com/nam000termux/mcservertermux/main/.bashrc")
  open(home+"/.bashrc", "wb").write(serverresponse.content)
  serverresponse = requests.get("https://raw.githubusercontent.com/nam000termux/mcservertermux/main/menu.py")
  open(home+"/menu.py", "wb").write(serverresponse.content)
  serverresponse = requests.get("https://raw.githubusercontent.com/nam000termux/mcservertermux/main/start.sh")
  open("/sdcard/mcsv/start.sh", "wb").write(serverresponse.content)
  os.system("chmod +x /sdcard/mcsv/start.sh")
  serverresponse = requests.get("https://github.com/nam000termux/mcservertermux/releases/download/Update/ZArchiverPro.apk")
  open("/sdcard/ZArchiverPro.apk", "wb").write(serverresponse.content)

os.system("clear")
if not "-noupdate" in sys.argv:
  print("Nhập lệnh mcsv -start để mở menu và bật server")
