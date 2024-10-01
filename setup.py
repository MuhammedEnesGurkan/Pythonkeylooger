from cx_Freeze import setup, Executable

# Yürütülebilir dosyanın yapılandırılması
executables = [Executable("server.py", target_name="server.exe")]

# Paket bağımlılıkları ve diğer ayarlar
setup(
    name="ServerApp",
    version="0.1",
    description="Sunucu uygulaması",
    executables=executables
)
