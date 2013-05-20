set @orig_lat=50.95;
set @orig_lon=6.966;
set @dist=10;
SELECT *, 3956 * 2 * ASIN(SQRT( POWER(SIN((@orig_lat - abs(  dest.lat)) * pi()/180 / 2),2) + COS(@orig_lat * pi()/180 ) * COS(  abs (dest.lat) *  pi()/180) * POWER(SIN((@orig_lon – dest.lon) *  pi()/180 / 2), 2) )) as distance FROM hk dest HAVING distance < @dist ORDER BY distance limit 10;




SELECT *, 3956 * 2 * ASIN(SQRT( POWER(SIN((50.95 - abs(  dest.lat)) * pi()/180 / 2),2) + COS(50.95 * pi()/180 ) * COS(  abs (dest.lat) *  pi()/180) * POWER(SIN((6.966 – dest.lon) *  pi()/180 / 2), 2) )) as distance FROM hk dest HAVING distance < 10 ORDER BY distance limit 10;
