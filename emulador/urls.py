from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="url_home_emulador"),
    path('esp32_s3/',views.fnctn_esp32_s3, name="url_esp32_s3"),

    path("esp32_s3/emulador/<int:id_Mntoramento>/ ", 
          views.fnctn_emulador_esp32_s3, 
          name="url_emulador_esp32_s3"
        ),    

    path("esp32_s3/emulador/dados/<int:id_assignment>/", 
          views.fnctn_dados_esp32_s3, 
          name="url_dados_esp32_s3"
        ),



    path('Rspbrry_PI_Pico_W/',views.fnctn_Rspbrry_PI_Pico_W, name="url_Rspbrry_PI_Pico_W"),

    path("Rspbrry_PI_Pico_W/emulador/<int:id_Mntoramento>/ ", 
          views.fnctn_emulador_Rspbrry_PI_Pico_W, 
          name="url_emulador_Rspbrry_PI_Pico_W"  #URL de acesso ao emulador Raspberry Pi Pico
        ),    
   
    path("Rspbrry_PI_Pico_W/emulador/dados/<int:id_assignment>/", 
          views.fnctn_dados_Rspbrry_PI_Pico_W, 
          name="url_dados_Rspbrry_PI_Pico_W"
        ),



    path("start-emldr_rspbrry_PI_Pico/", 
          views.fnctn_start_emldr_rspbrry_PI_Pico, 
          name="start_emulador"
        ),        
    path("pause-emldr_rspbrry_PI_Pico/", 
          views.fnctn_pause_emldr_rspbrry_PI_Pico, 
          name="pause_emulador"
        ),        
    path("resume-emldr_rspbrry_PI_Pico/", 
          views.fnctn_resume_emldr_rspbrry_PI_Pico, 
          name="resume_emulador"
        ),        
    path("stop-emldr_rspbrry_PI_Pico/", 
          views.fnctn_stop_emldr_rspbrry_PI_Pico, 
          name="stop_emulador"
        ),        
]
