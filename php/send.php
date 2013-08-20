<?php

class SMTPClient
{

function SMTPClient ($SmtpServer, $SmtpPort, $SmtpUser, $SmtpPass, $from, $to, $subject, $body)
{

$this->SmtpServer = $SmtpServer;
$this->SmtpUser = base64_encode ($SmtpUser);
$this->SmtpPass = base64_encode ($SmtpPass);
$this->from = $from;
if(strstr($to,","))
$this->to = explode(",",$to);
else
$this->to[] =$to;
$this->subject = $subject;
$this->body = $body;

if ($SmtpPort == "") 
{
$this->PortSMTP = 25;
}
else
{
$this->PortSMTP = $SmtpPort;
}
}

function SendMail ()
{
if ($SMTPIN = fsockopen ($this->SmtpServer, $this->PortSMTP)) 
{
fputs ($SMTPIN, "EHLO baofeng.com"."\r\n"); 
$talk["hello"] = fgets ( $SMTPIN, 1024 ); 
fputs($SMTPIN, "auth login\r\n");
$talk["res"]=fgets($SMTPIN,1024);
fputs($SMTPIN, $this->SmtpUser."\r\n");
$talk["user"]=fgets($SMTPIN,1024);
fputs($SMTPIN, $this->SmtpPass."\r\n");
$talk["pass"]=fgets($SMTPIN,256);
fputs ($SMTPIN, "MAIL FROM: <".$this->from.">\r\n"); 
$talk["From"] = fgets ( $SMTPIN, 1024 ); 
foreach($this->to as $t)
{
fputs ($SMTPIN, "RCPT TO: <".$t.">\r\n"); 
$talk["To"] = fgets ($SMTPIN, 1024); 
}
fputs($SMTPIN, "DATA\r\n");
$talk["data"]=fgets( $SMTPIN,1024 );
fputs($SMTPIN, "To: <".$this->to[0].">\r\nFrom: <".$this->from.">\r\nSubject:".$this->subject."\r\n\r\n\r\n".$this->body."\r\n.\r\n");
$talk["send"]=fgets($SMTPIN,256);
//CLOSE CONNECTION AND EXIT ... 
fputs ($SMTPIN, "QUIT\r\n"); 
fclose($SMTPIN); 
// 
} 
return $talk;
} 
}

$SmtpServer="mail.host.com";
$SmtpPort="25"; //default
$SmtpUser="user@host.com";
$SmtpPass="user";

if($_POST['to'])
{
$to = $_POST['to'];
$from = $SmtpUser;
$subject = $_POST['subject'];
$body = $_POST['body'];
$SMTPMail = new SMTPClient ($SmtpServer, $SmtpPort, $SmtpUser, $SmtpPass, $from, $to, $subject, $body);
$SMTPChat = $SMTPMail->SendMail();
}
print "ok";
