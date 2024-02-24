 var fin_date= "{{data.heure_fin }}";
 var heure_server= "{{heure }}";


function compareTime(time1, time2) {

    const date1 = new Date(`1970-01-01T${time1}Z`);
    const date2 = new Date(`1970-01-01T${time2}Z`);

    if (date1 < date2) { return -1; }
      else if  (date1 > date2) { return 1; }
         else { return 0; }
   }


    function checkTime() {
        var comparisonResult = compareTime(fin_date, heure_server);

        if (comparisonResult == -1 ){
            alert("Session du stream expirée")
            window.location.href = "/user/reservations"
         }

    }



   document.addEventListener("DOMContentLoaded", (event) => {
        setInterval(checkTime, 6000);

   });




   var msg_request =document.getElementById('request_msg')
   function submitForm(event) {
    event.preventDefault();
   msg_request.innerHTML="<span class='text-yellow-500'> <i class='fas fa-share'></i> Envoie du code...</span>"
    const form = document.getElementById('formulaire');
    const code = document.getElementById('code').value;
    const formData = new FormData();
    formData.append('code', document.getElementById('code').value)

      axios.post('/send_code', formData)
      .then(function (response) {
         if (response.data.status == true ) {
               msg_request.innerHTML="<span class='text-green-500'> <i class='fas fa-check-circle'></i> " + response.data.message + "</span>"
         }
           else{
               msg_request.innerHTML="<span class='text-red-500'> <i class='fas fa-exclamation-circle'></i> " + response.data.message + "</span>"
           }
      })
      .catch(function (error) {
      console.log(error)
         msg_request.innerHTML="<span class='text-red-500'> <i class='fas fa-exclamation-circle'></i>" + error + " </span>"
       });


}


const formElement = document.getElementById('formulaire');
formElement.addEventListener('submit', submitForm);
