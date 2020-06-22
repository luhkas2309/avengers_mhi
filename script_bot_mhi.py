from cx_Freeze import setup, Executable
 
setup(name='Bot Avengers',
    version='1.0',
    description='Programa desenvolvido por iniciativa Avengers',
    # options={'build_exe': {'packages': ['threading','time','logging','pytz','iqoptionapi','os','schedule','datetime','dateutil','sys','numpy','pip']}},
    executables = [Executable(
                   script='bot_mhi.py'
                   )
                  ]
)