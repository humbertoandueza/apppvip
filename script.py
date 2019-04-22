import mysql.connector
import json
from datetime import datetime
import calendar
import time
import datetime
import smtplib, ssl
today=datetime.datetime.now()
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mydb = mysql.connector.connect(
  host="vidaplena.mysql.pythonanywhere-services.com",
  user="vidaplena",
  passwd="01051998a",
  database="vidaplena$default"
)
consulata = mydb.cursor()

fecha = today.strftime("%Y-%m-%d")
#print (fecha)
consulata.execute("select a.nombre as actividad,a.lugar,a.descripcion,a.fecha,p.correo,p.nombre from actividades_actividades a inner join persona_persona p where a.fecha='"+fecha+"' and p.id=a.persona_id;")
resultado = consulata.fetchall()

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "humbertoanduezaa@gmail.com"
password = "01051998a"

# Create a secure SSL context
context = ssl.create_default_context()
def mail(data):
	# Try to log in to server and send email
	try:
		server = smtplib.SMTP(smtp_server,port)
		server.ehlo() # Can be omitted
		server.starttls() # Secure the connection
		server.ehlo() # Can be omitted
		server.login(sender_email, password)
		for i in data:
			message = MIMEMultipart("alternative")
			message["Subject"] = "AppVip Notificación"


			# Create the plain-text and HTML version of your message
			html = """\
			<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <table cellpadding="0" cellspacing="0" border="0" align="center" style="background-color:#f9f9f9;border-collapse:collapse;line-height:100%!important;margin:0;padding:0;width:100%!important" bgcolor="#f9f9f9">
        <tbody>
            <tr>
                <td>
                    <table style="border-collapse:collapse;margin:auto;max-width:635px;min-width:320px;width:100%" class="m_5191768325981104092main-wrap">
                        <tbody>
                            <tr>
                                <td valign="top">
                                    <table cellpadding="0" cellspacing="0" border="0" class="m_5191768325981104092reply_header_table" style="border-collapse:collapse;color:#c0c0c0;font-family:'Helvetica Neue',Arial,sans-serif;font-size:13px;line-height:26px;margin:0 auto 26px;width:100%">
                                    </table>
                                </td>
                            </tr>
                            <tr>
                                <td valign="top" style="padding:0 20px">
                                    <table cellpadding="0" cellspacing="0" border="0" align="center" style="background-clip:padding-box;border-collapse:collapse;border-radius:3px;color:#545454;font-family:'Helvetica Neue',Arial,sans-serif;font-size:13px;line-height:20px;margin:0 auto;width:100%">
                                        <tbody>
                                            <tr>
                                                <td valign="top">
                                                    <table cellpadding="0" cellspacing="0" border="0" style="border:none;border-collapse:separate;font-size:1px;height:2px;line-height:3px;width:100%">
                                                        <tbody>
                                                            <tr>
                                                                <td valign="top" style="background-color:#40A85D;border:none;font-family:'Helvetica Neue',Arial,sans-serif;width:100%" bgcolor="#40A85D">&nbsp;</td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                    <table cellpadding="0" cellspacing="0" border="0" style="background-clip:padding-box;border-collapse:collapse;border-color:#dddddd;border-radius:0 0 3px 3px;border-style:solid solid none;border-width:0 1px 1px;width:100%">
                                                        <tbody>
                                                            <tr>
                                                                <td style="background-clip:padding-box;background-color:white;border-radius:0 0 3px 3px;color:#525252;font-family:'Helvetica Neue',Arial,sans-serif;font-size:15px;line-height:22px;overflow:hidden;padding:40px 40px 30px" bgcolor="white">
                                                                    <div style="margin-bottom:16px;margin-top:0;padding-top:0;text-align:center!important" align="center">

                                                                        <img src="https://vidaplena.pythonanywhere.com/static/images/logo.png" alt="APPVIP" width="180" onclick="return false;" style="margin:17px 0;max-width:60%">
                                                                    </div>
                                                                    <h2 style="color:#282f33;font-size:18px;font-weight:bold;margin:30px 0 7px;text-align:center!important" align="center">
                                                                        Hola {}
                                                                    </h2>
                                                                    <p>Te recordamos que hoy tienes una actividad pendiente por realizar.</p>
                                                                    <p>Nombre: {}</p>
                                                                    <p>Descripcion: {}.</p>
                                                                    <p>Lugar: {}.</p>

                                                                    <p>¡Visitanos ya! <br>
                                                                    </p>
                                                                    <!-- <p style="line-height:1.5;margin:0 0 17px;text-align:left!important" align="left">

                                                                    </p>
                                                                    <p style="line-height:1.5;margin:0 0 17px;text-align:left!important" align="left">Telotengo</p> -->
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>

                                    <div style="display:none;height:0;max-height:0;max-width:0;opacity:0;overflow:hidden;width:0">
                                        <table cellpadding="0" cellspacing="0" border="0" align="center" style="border-collapse:collapse;color:#545454;display:none;font-family:'Helvetica Neue',Arial,sans-serif;font-size:13px;height:0;line-height:20px;margin:0 auto;max-height:0;max-width:100%;opacity:0;overflow:hidden;width:100%">
                                            <tbody>
                                                <tr>
                                                    <td valign="top" width="80" style="color:#272727;height:18px;padding-left:40px;text-align:left" align="left">
                                                        <img alt="Triangle" height="18" src="https://ci4.googleusercontent.com/proxy/9Y1p5EWpjsisMhMUd9iRWBGSpCCzryQp9437rQYtk9fHQCqD3v0QXECLRlIEEDj9fpWGPiOKTWOEg5nKV1-hkYIVpzTmot4bPgS9jou00ShxYQlxF1EKNnUXKyba1xhXrNoF-0t5E9jf6NR1-BJ1LfJKzY5t_qM08f7pOESk=s0-d-e1-ft#https://marketing.intercomassets.com/assets/email/personal/triangle-8747882e9ef8882f9bc057241fd3c049.png" style="display:inline-block;max-width:100%;outline:none;text-decoration:none" width="40">
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <div>
                                        <table cellpadding="0" cellspacing="0" border="0" align="center" style="border-collapse:collapse;margin:0 auto;max-width:100%;width:100%">
                                            <tbody>
                                                <tr>
                                                    <td valign="top" width="100%">
                                                        <img alt="arrow" src="https://ci5.googleusercontent.com/proxy/Wk07so5PXq8lsSwIUO9c6ah52RLjXWk7k2BErhQH_i6_zPLk9Q4si6YDsfkgAhE6IvUpjRmPRjPCWPeC01WAUiiFclRdCpUQWzpXH43-YUjPRSPGweOtYg32zpyIwPjzEbJJNCqdozRICpO9jGnYNwwJd2NQGeK1HA8LDLmk0S8SCDaxeK-FfGv_Se0LHYSH-5Kg6DCc1e599qBF=s0-d-e1-ft#https://marketing.intercomassets.com/assets/email/personal/arrow-37f6774809df6fd083bfc98e9d562e23ca6ede618e2b5e10c042de88d2f858dd.png" style="max-width:100%;width:100%">
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>

                                    <table cellpadding="0" cellspacing="0" border="0" align="center" style="border-collapse:collapse;color:#545454;font-family:'Helvetica Neue',Arial,sans-serif;font-size:13px;line-height:20px;margin:0 auto;max-width:100%;width:100%">
                                        <tbody>
                                            <tr>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                        <tbody>
                                            <tr>
                                                <td width="75%">
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;color:#545454;font-family:'Helvetica Neue',Arial,sans-serif;font-size:13px;line-height:20px;margin:0 auto;max-width:100%;width:100%">
                                                        <tbody>
                                                            <tr>
                                                                <td width="40">&nbsp;</td>
                                                                <td valign="middle" width="50" style="color:#272727" align="left"
                                                                    <span class="HOEnZb">
                                                                      <font color="#888888"></font>
                                                                  </span>
                                                              </td>
                                                              <td style="color:#999999">
                                                              &copy; 2019 - AppVip</span>
                                                          </td>
                                                      </tr>
                                                  </tbody>
                                              </table>
                                          </td>
                                      </tr>
                                  </tbody>
                              </table>
                          </td>
                      </tr>
                  </tbody>
              </table>
          </td>
      </tr>
      <tr>
        <td valign="top" height="20"></td>
    </tr>
</tbody>
</table>
</body>
</html>
			""".format(i[5],str(i[0]),i[2],i[1])

			# Turn these into plain/html MIMEText objects
			#part1 = MIMEText(text, "plain")
			part2 = MIMEText(html, "html")

			# Add HTML/plain-text parts to MIMEMultipart message
			# The email client will try to render the last part first
			#message.attach(part1)
			message.attach(part2)
			print('enviando mensaje a ',i[4])
			server.sendmail(sender_email, "wiliexyandreina@gmail.com",message.as_string())
			# TODO: Send email here
	except Exception as e:
	    # Print any error messages to stdout
	    print(e)
	finally:
		server.quit()
if len(resultado)>0:
    print('Si hay actividades pendientes el dia de hoy')
    mail(resultado)
else:
    print('No hay actividades pendientes el dia de hoy')




