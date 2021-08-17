# Steps to obtaining CMIP5 data from ESG.

[0.] Install JDK (requires admin. permissions, so you shouldn't have to do this unless you are downloading to your own computer)  
(http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html).
-----
1. Make sure your lim-corr repo is up-to-date. This will give you
access to a script called retriever.py.  
2. Run `retriever.py —help` to get a list of options.  
3. If successful, this will generate a wget
script with your request in the folder ${LIM_CORR_ROOT}/data. It will
be called something `like fetch_atmos_CMIP5_CCSM4_tas_historical_mon_r1i1p1.sh`.  
4. Run the script you just created (eventually this will all be internally handled by python) with the
`-H` flag like this (assuming you are in the same directory as the script):  
```bash fetch_atmos_CMIP5_CCSM4_tas_historical_mon_r1i1p1.sh -H```  
5. You will be prompted for your "openID:"
`Please give your OpenID (Example: https://myserver/example/username) ?`
6.a If you have registered with ESG one of the CMIP5 nodes  
__VERY IMPORTANT__: www.earthsystemgrid.org does not work for retrieving CMIP5
data. So if you registered there, you will have to register again at
the PCMDI, or other, node.
6.b You cal also just used the shared openID for our lab:  
    https://esgf-node.llnl.gov/esgf-idp/openid/ecrl-user  
7. Enter the password sent to you via https://cornell.app.box.com.  
8. Cross fingers and wait...  
9. And if you see something like this, you will know you were successful:  

```
  md5 ok. done!
done
```




