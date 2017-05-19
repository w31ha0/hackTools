 <?php
	
$ip = $_SERVER['REMOTE_ADDR'];
	
$arp = "/usr/sbin/arp"; // execute the arp command to get their mac address
	
$mac = shell_exec("sudo $arp -an " . $ip);
	
preg_match('/..:..:..:..:..:../',$mac , $matches);
	
$mac = @$matches[0];
	
if( $mac === NULL) {
		
    echo "Access Denied."; exit;
	
}
	
$cmd = "sudo iptables -t mangle -I internet 1 -m mac --mac-source ".$mac." -j RETURN";
	
shell_exec($cmd);
	
?>

<style>
img{
position: fixed; right: 0; bottom: 0;
min-width: 100%; min-height: 100%;
width: auto; height: auto; z-index: -100;
background: url(polina.jpg) no-repeat;

background-size: cover;
}
</style>
<img src="kid.jpg">
<video autoplay>
<source src="video" type="video/mp4">
</video> 