function notify(message, status, duration=7){
  if (status == true){
    alertify.success(message, duration);
  }
  else if (status == false){
    alertify.error(message, duration);
  }
  else{
    alertify.message(message, duration);
  }
}
