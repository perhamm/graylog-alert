<?php

$jsonString = file_get_contents("php://input");
$json = json_decode($jsonString);

$messages = '';
$header = '';
$header_ver2 = '';
$messages_ver2 = '';

if (!empty($json->check_result->matching_messages)) {$messages = $json->check_result->matching_messages;}
if (!empty($json->check_result->triggered_condition->title)) {$header = $json->check_result->triggered_condition->title;}
if (!empty($json->event_definition_title)) {$header_ver2 = $json->event_definition_title;}
if (!empty($json->backlog)) {$messages_ver2 = $json->backlog;}
$log = "post.log";
file_put_contents($log,$jsonString,FILE_APPEND);
file_put_contents($log,"\n",FILE_APPEND);
$text = "";



define('TELEGRAM_TOKEN', 'аоыдваывалдывалдывалдоывдлаодывлаодываываываыва');



function message_to_telegram($text,$chat_id) {

	$command = 'python tlgrm.py  ' . $chat_id. ' "' . $text. '"' ;
	$python = `$command`;



}


function message_to_email($type,$body,$log) {

	$command = 'python grlemail.py  '.$type.' "'.$body.'"';
	file_put_contents($log,"Выполняю следующее:\n",FILE_APPEND);
	file_put_contents($log,$command."\n",FILE_APPEND);
	$python = `$command`;



}


if ($header == '!APC! Что-то с UPS')
{
		
	$header = "🔌 !APC! Что-то с UPS"."\xA"."\xA";
	
	foreach($messages as $message_body) {
	
	$text .= '⚠️ '.$message_body->message."\xA".$message_body->timestamp."\xA";
	
	}
	
	file_put_contents($log,"Отправляю следующее:\n",FILE_APPEND);
	file_put_contents($log,$header.$text."\n"."-аывавваываываываываыва"."\n",FILE_APPEND);
	message_to_telegram($header.$text,'-аывавваываываываываыва');
	
	//echo exec('zabbix_get -s 10.209.101.170 -k terrorist'); 
	
}

if ($header == 'CheckPoint Remote Login')
{
		
	
	
	foreach($messages as $message_body) {
		
	
	$user = "USER:".$message_body->fields->User."\xA";
	$src = "SRC:".$message_body->fields->src."\xA";
	$ip_data = @json_decode(file_get_contents("http://ip-api.com/json/".$message_body->fields->src));
	$city = '';
	$country = '';
	$asprov = '';
	$org = '';
	$os_name = '';
	$host_type = '';
	$client_version = '';
	$client_name = '';
	if (!empty($message_body->fields->os_name)) {$os_name = "os_name:".$message_body->fields->os_name."\xA";}
	if (!empty($message_body->fields->host_type)) {$host_type = "host_type:".$message_body->fields->host_type."\xA";}
	if (!empty($message_body->fields->client_version)) {$client_version = "client_version:".$message_body->fields->client_version."\xA";}
	if (!empty($message_body->fields->client_name)) {$client_name = "CLIENT_NAME:".$message_body->fields->client_name."\xA";}
	//$login_timestamp = "login_timestamp:".$message_body->fields->login_timestamp."\xA";
	if (!empty($message_body->fields->client_name)) {if (strpos($message_body->fields->client_name, 'Endpoint Security') !== false )  {$header = "\xA"."💻Уведомление об удаленном подключении📣"."\xA";} else {$header = "\xA"."📲Уведомление об удаленном подключении📣"."\xA";} }
	file_put_contents($log,"Отправляю следующее:\n",FILE_APPEND);
	$ip_data_city = '';
	if (!empty($ip_data->city)) {$ip_data_city = $ip_data->city;}
	if($ip_data && $ip_data_city != null)
	{
		$city = "city:".$ip_data->city."\xA";
		$country = "country:".$ip_data->country."\xA";
		$asprov = "as:".$ip_data->as."\xA";
		$org = "org:".$ip_data->org."\xA";
		file_put_contents($log,$header.$user.$src.$os_name.$host_type.$client_version.$client_name.$city.$country.$asprov.$org."\n"."-аывавваываываываываыва"."\n",FILE_APPEND);
		message_to_telegram($header.$user.$src.$os_name.$host_type.$client_version.$client_name.$city.$country.$asprov.$org,'-аывавваываываываываыва');
	}
	else
	{
		file_put_contents($log,$header.$user.$src.$os_name.$host_type.$client_version.$client_name."\n"."-аывавваываываываываыва"."\n",FILE_APPEND);
		message_to_telegram($header.$user.$src.$os_name.$host_type.$client_version.$client_name,'-аывавваываываываываыва');
	}
	
	}


	
}


if ($header == 'CheckPoint Login Failure')
{
		
	
	
	foreach($messages as $message_body) {
		
	
	$user = "USER:".$message_body->fields->User."\xA";
	$src = "SRC:".$message_body->fields->src."\xA";
	$ip_data = @json_decode(file_get_contents("http://ip-api.com/json/".$message_body->fields->src));
	$city = '';
	$country = '';
	$asprov = '';
	$org = '';
	$os_name = '';
	$client_version = '';
	$client_name = '';
	if (!empty($message_body->fields->os_name)) {$os_name = "os_name:".$message_body->fields->os_name."\xA";}
	if (!empty($message_body->fields->client_version)) {$client_version = "client_version:".$message_body->fields->client_version."\xA";}
	if (!empty($message_body->fields->client_name)) {$client_name = "CLIENT_NAME:".$message_body->fields->client_name."\xA";}
	//$login_timestamp = "login_timestamp:".$message_body->fields->login_timestamp."\xA";
	$reason = "REASON:".$message_body->fields->reason."\xA";
	$header = "\xA"."😈Неудачная попытка удаленного подключения📣"."\xA";
	file_put_contents($log,"Отправляю следующее:\n",FILE_APPEND);
	$ip_data_city = '';
	if (!empty($ip_data->city)) {$ip_data_city = $ip_data->city;}
	if($ip_data && $ip_data_city != null)
	{
		$city = "city:".$ip_data->city."\xA";
		$country = "country:".$ip_data->country."\xA";
		$asprov = "as:".$ip_data->as."\xA";
		$org = "org:".$ip_data->org."\xA";
		file_put_contents($log,$header.$user.$src.$os_name.$client_version.$client_name.$reason.$city.$country.$asprov.$org."\n"."-аывавваываываываываыва"."\n",FILE_APPEND);
		message_to_telegram($header.$user.$src.$os_name.$client_version.$client_name.$reason.$city.$country.$asprov.$org,'-аывавваываываываываыва');
	}
	else
	{
		file_put_contents($log,$header.$user.$src.$os_name.$client_version.$client_name.$reason."\n"."-аывавваываываываываыва"."\n",FILE_APPEND);
		message_to_telegram($header.$user.$src.$os_name.$client_version.$client_name.$reason,'-аывавваываываываываыва');
	}
	}


	
}

if ($header == 'smbscan')
{
		
	
	
	foreach($messages as $message_body) {
		
	

	$src = "SRC: ".$message_body->fields->src."\xA";
	$src_dns_name = gethostbyaddr ( $message_body->fields->src );
	$src_dns =  '';
	if ($message_body->fields->src !== $src_dns_name ) {$src_dns = "src name: ".$src_dns_name."\xA";} else {$src_dns = "src name: Non-existent domain"."\xA";}
	$dst = "DST: ".$message_body->fields->dst."\xA";
	$dst_machine_name = '';
	$dst_user_name = '';
	if (!empty($message_body->fields->dst_machine_name)) {$dst_machine_name = "dst name: ".$message_body->fields->dst_machine_name."\xA";} else {$dst_dns_name = gethostbyaddr ( $message_body->fields->dst ); if($dst_dns_name !== $message_body->fields->dst ) {$dst_machine_name = "dst name: ".$dst_dns_name."\xA";} else {$dst_machine_name = "dst name: Non-existent domain"."\xA";}}
	if (!empty($message_body->fields->dst_user_name)) {$dst_user_name = "dst user: ".$message_body->fields->dst_user_name."\xA";}
	$header = "\xA"."🚩 SMB Scan Detected☝"."\xA";
	file_put_contents($log,"Отправляю следующее:\n",FILE_APPEND);
	file_put_contents($log,$header.$src.$src_dns.$dst.$dst_machine_name.$dst_user_name."\n"."-аывавваываываываываыва"."\n",FILE_APPEND);
	message_to_telegram($header.$src.$src_dns.$dst.$dst_machine_name.$dst_user_name,'-аывавваываываываываыва');
	
	}


	
}



if ($header == 'ips')
{
		
	
	
	foreach($messages as $message_body) {
		
	$Name = '';
	$resource = '';
	$Info = '';
	$reason = '';
	$attack = '';
	$src = '';
	$src_n = '';
	$dst = '';
	$dst_n = '';
	
	if (!empty($message_body->fields->Name)) {$Name = "Name: ".$message_body->fields->Name."\xA";}
	if (!empty($message_body->fields->resource)) {$resource = "resource: ".$message_body->fields->resource."\xA";}
	if (!empty($message_body->fields->Info)) {$Info = "Info: ".$message_body->fields->Info."\xA";}
	if (!empty($message_body->fields->reason)) {$reason = "reason: ".$message_body->fields->reason."\xA";}
	if (!empty($message_body->fields->attack)) {$attack = "attack: ".$message_body->fields->attack."\xA";}
	if (!empty($message_body->fields->src)) {$src = "src: ".$message_body->fields->src."\xA";}
	if (!empty($message_body->fields->src)) {$src_n = gethostbyaddr ( $message_body->fields->src );}
	if (!empty($message_body->fields->src)) {if ($src_n !== $message_body->fields->src ) {$src_n = "src name: ".$src_n."\xA";} else {$src_n = "src name: Non-existent domain"."\xA";}}
	if (!empty($message_body->fields->dst)) {$dst = "dst: ".$message_body->fields->dst."\xA";}
	if (!empty($message_body->fields->dst)) {$dst_n = gethostbyaddr ( $message_body->fields->dst );}
	if (!empty($message_body->fields->dst)) {if ($dst_n !== $message_body->fields->dst ){$dst_n = "dst name: ".$dst_n."\xA";} else {$dst_n = "dst name: Non-existent domain"."\xA";}	}
	
	
	$header = "\xA"."👻IPS Log detect☝"."\xA";
	file_put_contents($log,"Отправляю следующее:\n",FILE_APPEND);
	file_put_contents($log,$header.$Name.$resource.$Info.$reason.$attack.$src.$src_n.$dst.$dst_n."\n"."-1001495027732"."\n",FILE_APPEND);
	message_to_telegram($header.$Name.$resource.$Info.$reason.$attack.$src.$src_n.$dst.$dst_n,'-1001495027732');
	
	}


	
}


if ($header == 'paloaltoscan')
{
		
	
	
	foreach($messages as $message_body) {
		
	$action = '';
	$srcip = '';
	$srcname = '';
	$date = '';
	$from = '';
	$to = '';
	$threattype = '';
	$threatdesc = '';
	$from_user = '';
	$dstip = '';
	$dstname = '';



	
	if (!empty($message_body->fields->action)) {$action = "Action: ".$message_body->fields->action."\xA";}
	
	if (!empty($message_body->fields->srcip)) {$srcip = "srcip: ".$message_body->fields->srcip."\xA";}
	if (!empty($message_body->fields->srcip)) {$srcname = gethostbyaddr ( $message_body->fields->srcip );}
	if (!empty($message_body->fields->srcip)) {if ($srcname !== $message_body->fields->srcip ) {$srcname = "src name: ".$srcname."\xA";} else {$srcname = "src name: Non-existent domain"."\xA";}}

	if (!empty($message_body->fields->date)) {$date = "date: ".$message_body->fields->date."\xA";}
	if (!empty($message_body->fields->from)) {$from = "from: ".$message_body->fields->from."\xA";}
	if (!empty($message_body->fields->to)) {$to = "to: ".$message_body->fields->to."\xA";}

	if (!empty($message_body->fields->threattype)) {$threattype = "threattype: ".$message_body->fields->threattype."\xA";}
	if (!empty($message_body->fields->threatdesc)) {$threatdesc = "threatdesc: ".$message_body->fields->threatdesc."\xA";}

	if (!empty($message_body->fields->from_user)) {$from_user = "from_user: ".$message_body->fields->from_user."\xA";}
	
	
	if (!empty($message_body->fields->dstip)) {$dstip = "dstip: ".$message_body->fields->dstip."\xA";}
	if (!empty($message_body->fields->dstip)) {$dstname = gethostbyaddr ( $message_body->fields->dstip );}
	if (!empty($message_body->fields->dstip)) {if ($dstname !== $message_body->fields->dstip ) {$dstname = "dst name: ".$dstname."\xA";} else {$dstname = "dst name: Non-existent domain"."\xA";}}
	
	$header = "\xA"."😈Зафиксирован скан сети☝"."\xA";
	file_put_contents($log,"Отправляю следующее:\n",FILE_APPEND);
	file_put_contents($log,$header.$action.$srcip.$srcname.$date.$from.$to.$threattype.$threatdesc.$from_user.$dstip.$dstname."\n"."-аывавваываываываываыва"."\n",FILE_APPEND);
	message_to_telegram($header.$action.$srcip.$srcname.$date.$from.$to.$threattype.$threatdesc.$from_user.$dstip.$dstname,'-аывавваываываываываыва');
	
	}


	
}



if ($header_ver2 == 'SpamKasperFilter')
{
		
	
	foreach($messages_ver2 as $message_body) {
		
		$type = "spam";
		if (!empty($message_body->fields->full_message)) {
			

			$string = str_replace("\n", "|", $message_body->fields->full_message);
			$string = str_replace("\r", "|", $string );
			file_put_contents($log,"Отправляю следующее:\n",FILE_APPEND);
			file_put_contents($log,$type." ".$string."\n",FILE_APPEND);

			message_to_email($type,$string,$log);
		}
	

	}

}


//message_to_telegram("\xA"."👻IPS Log detect☝"."\xA"."\xA"."👻IPS Log detect☝"."\xA"."\xA"."👻IPS Log detect☝"."\xA"."\xA"."👻IPS Log detect☝"."\xA"."\xA"."👻IPS Log detect☝"."\xA",'134143419');

?>
