

function loadData() {
    fetch('http://localhost:3333/v2/web/api/booking/cityadd', {
  method: 'GET',
  headers: {
    'x-Origin-Key': 'gAAAAABjuCeqGUoHO5p5iIu1XMX_5sxKKJEgrEW6OP3QvmrXiYw4XtpT7Ta1kvLVzIgHMvBHSKH2LHvG52lsaRXeXSuN2LD4z7-4frOA_bbsJH-gjaV175Y=',
'x-Api-Key': 'gAAAAABjuCeqjgSygMlxl2p6S--F5X8tpxKua3uGl8OKsXzs4j9cMlILABVfRD1u16rRYzCUmKRDB7V3Zr-aetrYMU63P-X_bjuqIFiwyougmPKE1ntRU6A=',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJnQUFBQUFCanVDZXFUQTBacy1WM3E2eVF4ZF9uQjJyd1Bva01pRU5HNjJmczNwaVNFaGxfLUU3aEJyWWxSYS1KT29sc2xiN1Q3WFRCeWcwM3pMRk5XQV81X1lEOTJ6OFZQWWVKa3ZiSnFrckNUU1R6b3ZUM1l2QT0iLCJleHAiOjE3MDQ1NDkxNjJ9.ulk8BRP3KH60fjOJgjRdQ3IxT5UtFXKytPVyrgJfyNA',
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
'Access-Control-Allow-Methods': 'GET'
  },
  
})
  .then(response => response.json())
  .then(data => {
    // Do something with the data
    document.getElementById('result').innerHTML = data.key
  })
  .catch(error => {
    console.error(error)
  })
  }
  
