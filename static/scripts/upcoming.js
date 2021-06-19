function setupData() {
  $(document).ready(function () {
    console.log("aasasasasas");
    // alert('i am inside')
    var table = $("#upcomingInterviewsDataTable").DataTable({
      processing: true,
      deferRender: true,
      ajax: {
        url: "/getUpcomingData",
        dataSrc: "",
        type: "GET",
        dataType: "json",
      },
      columnDefs: [{ className: "text-center align-middle", targets: "_all" }],
      columns: [
        { data: "name" },
        { data: "email" },
        { data: "phone" },
        { data: "availableon" },
        { data: "scheduleTime" },
        {
          data: 'resumeURL',
          render: function(data) {
              return '<a href='+ data +" "+'target="_blank">Click me!</a>'
          }
      },
        {
          data: null,
          defaultContent:
          '<button type="button" class="info btn btn-sm btn-info"><i class="fa fa-eye"></i></button>&nbsp&nbsp'
        },
      ],
    });
    $("#upcomingInterviewsDataTable").on("click", ".info", function (e) {
      var data = table.row($(this).parents("tr")).data();
      // var row = this.parentNode.parentNode;
      var confirmalert = confirm("Do you want to view " + data.email + " | " + data.name + " ?");
      if (confirmalert == true) {
        alert(data);
        $.ajax({
          url: "viewUpcoming",
          contentType: "application/json;charset=utf-8",
          type: "POST",
          traditional: "true",
          data: JSON.stringify({ data }),
          dataType: "json",
          success: function (results, textStatus) {
            if (results.sucess) {
              console.log(data);
              window.location.href = "viewUpcoming";
            } else {
              console.log("no redirect");
            }
          },
          error: function (error) {
            alert(error);
          },
        });
      }
    });
  });
}
$(window).on("load", setupData);