<?php
#set appropriate content type - to tell the browser we're returning Javascript
header( 'Content-Type: text/javascript' );         

# start the session
session_start();           

$lat = $_POST['lat'];
$lon = $_POST['lon'];
$dist = $_POST['dist'];
$LIMIT = 3;

//print "Input: $lat <br/> $lon <br/> $dist <br/>";


try {
    $user = 'web1294';
    $pass = trim(file_get_contents('../../../files/dbpass'));
    if( $pass === True ){
        die("Could not read DB password file");
    }
    $dbh = new PDO('mysql:host=localhost;dbname=usr_web1294_6', $user, $pass);
    
    $setlat = $dbh->prepare("set @orig_lat=:lat");
    $setlat->bindParam(':lat', $lat);
    $rc = $setlat->execute();

    //if( $rc === False){
    //    print "Erro executing statment setlat";
    //}
    $setlon = $dbh->prepare("set @orig_lon=:lon");
    $setlon->bindParam(':lon', $lon);
    $rc = $setlon->execute();

    //if( $rc === False){
    //    print "Erro executing statment";
    //}
    $setdist = $dbh->prepare("set @dist=:max_dist");
    $setdist->bindParam(":max_dist", $dist, PDO::PARAM_INT);
    $rc = $setdist->execute();

    //if( $rc === False){
    //    print "Erro executing statment setdist";
    //}
    $stmt = $dbh->prepare("SELECT *, 3956 * 2 * ASIN(SQRT( POWER(SIN((@orig_lat - abs(  dest.lat)) * pi()/180 / 2),2) + COS(@orig_lat * pi()/180 ) * COS(  abs (dest.lat) *  pi()/180) * POWER(SIN((@orig_lon - dest.lon) *  pi()/180 / 2), 2) )) as distance FROM ice dest HAVING distance < @dist ORDER BY distance limit :nrow");
    $stmt->bindParam(':nrow', $LIMIT, PDO::PARAM_INT); 
    $rc = $stmt->execute();

    //if( $rc === False){
    //    print "Erro executing statment select";
    //}

    $query_res = $stmt->fetchAll();
    if (empty($query_res)) {
        $result = array("success" => False);
    }else{
        $result["success"] = True;
    }

    $result["user"] = array("lat"=>$lat, "lon"=>$lon, "dist"=>$dist);
    $result["results"] = $query_res;
    print(json_encode($result));

    //foreach($result as $array){

    //    foreach ($array as $key => $value){
    //        print $key. "=>".$value ."<br/>";
    //    }
    //    print "<br/>";
    //}
    //print "<br/>";

    $dbh = null;
} catch (PDOException $e) {
    #print "Error!: " . $e->getMessage() . "<br/>";
    //print "Database error <br/>";
    $result = array("success" => False);
    print(json_encode($result));
    die();
}
?>
