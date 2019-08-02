function sms() {
  var locale = $("#locale").val();
  $.post("/authy/sms", {locale: locale}, function(data) {
    if (data.success) {
      alert("sent authy sms 2.0");
      console.log("sent authy sms2.0");
    };
  });
};


function voice() {
  var locale = $("#locale").val();
  $.post("/authy/voice", {locale: locale}, function(data) {
    if (data.success) {
        alert("sent authy voice call");
        console.log("sent authy voice call");
    };
  });
}

$(document).ready(function() {
  $("#send-push").on("click", function(e) {
    e.preventDefault();
    startPushAuthentication();
  });

  var startPushAuthentication = function() {
    $.post("/authy/push", function(data) {
      if (data.success) {
        checkPushStatus(data.uuid);
      }
    });
  };

  var checkPushStatus = function(uuid) {
    $.get("/authy/push/status?uuid=" + uuid, function(data) {
      if (data.status == "approved") {
        alert("approved");
        window.location.href = "/authy/protected"
      } else if (data.status == "denied") {
        alert("denied");
      } else {
        setTimeout(checkPushStatus(uuid), 10000);
      }
    });
  };
});
