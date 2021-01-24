var user_tickets_endpoint = "/api/user_ticket_status";

$.ajax({
    method: "GET",
    url: user_tickets_endpoint,
    success: function (data) {
        setUserChart(data);
        console.log()
    },
    error: function (error) {
        emptyCall()
    },
});

var pm_tickets_overview_endpoint = "/api/pm_tickets_overview";

$.ajax({
    method: "GET",
    url: pm_tickets_overview_endpoint,
    success: function (data) {
        setPmTicketsChart(data);
        console.log(data.dataset)
    },
    error: function (error) {
        emptyCall()
    },
});



function setPmTicketsChart(data) {

    var ctx = document.getElementById('pm_chart').getContext('2d');
    Chart.defaults.global.defaultFontColor = 'rgba(255,255,255,0.8)';


    var gradientFill = ctx.createLinearGradient(0, 1000, 0, 0);
    gradientFill.addColorStop(1, "rgba(148,25,39,0.2)");
    gradientFill.addColorStop(0.5, "rgba(148,25,39,0.1)");
    gradientFill.addColorStop(0, "rgba(148,25,39,0)");

    var gradientFill2 = ctx.createLinearGradient(0, 1000, 0, 0);
    gradientFill2.addColorStop(1, "rgba(249, 99, 50,0.2)");
    gradientFill2.addColorStop(0.5, "rgba(249, 99, 50,0.1)");
    gradientFill2.addColorStop(0, "rgba(249, 99, 50,0)");

    var gradientFill3 = ctx.createLinearGradient(0, 1000, 0, 0);
    gradientFill3.addColorStop(1, "rgba(0,0,255,0.2)");
    gradientFill3.addColorStop(0.5, "rgba(0,0,255,0.1)");
    gradientFill3.addColorStop(0, "rgba(0,0,255,0)");

    var gradientFill4 = ctx.createLinearGradient(0, 1000, 0, 0);
    gradientFill4.addColorStop(1, "rgba(0,128,0,0.2)");
    gradientFill4.addColorStop(0.5, "rgba(0,128,0,0.1)");
    gradientFill4.addColorStop(0, "rgba(0,128,0,0)");


    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [

                {
                    label: ['1', '2', '3', '4',],
                    data: ['1', '1', '1', '1',],
                },
                {
                    label: ['1', '2', '3', '4',],
                    data: ['1', '1', '1', '1',],
                },
                {
                    label: ['1', '2', '3', '4',],
                    data: ['1', '1', '1', '1',],
                },
                {
                    label: ['1', '2', '3', '4',],
                    data: ['1', '1', '1', '1',],
                },

            ]
        },
        options: {
            legend: {
                display: false
            }
        }

    });
}




function setUserChart(data) {
    var ctx = document.getElementById('myChart').getContext('2d');
    Chart.defaults.global.defaultFontColor = 'rgba(255,255,255,0.8)';


    var gradientFill = ctx.createLinearGradient(0, 1000, 0, 0);
    gradientFill.addColorStop(1, "rgba(148,25,39,0.2)");
    gradientFill.addColorStop(0.5, "rgba(148,25,39,0.1)");
    gradientFill.addColorStop(0, "rgba(148,25,39,0)");

    var gradientFill2 = ctx.createLinearGradient(0, 1000, 0, 0);
    gradientFill2.addColorStop(1, "rgba(249, 99, 50,0.2)");
    gradientFill2.addColorStop(0.5, "rgba(249, 99, 50,0.1)");
    gradientFill2.addColorStop(0, "rgba(249, 99, 50,0)");

    var gradientFill3 = ctx.createLinearGradient(0, 1000, 0, 0);
    gradientFill3.addColorStop(1, "rgba(0,0,255,0.2)");
    gradientFill3.addColorStop(0.5, "rgba(0,0,255,0.1)");
    gradientFill3.addColorStop(0, "rgba(0,0,255,0)");

    var gradientFill4 = ctx.createLinearGradient(0, 1000, 0, 0);
    gradientFill4.addColorStop(1, "rgba(0,128,0,0.2)");
    gradientFill4.addColorStop(0.5, "rgba(0,128,0,0.1)");
    gradientFill4.addColorStop(0, "rgba(0,128,0,0)");


    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.label,
            datasets: [{
                label: 'Tickets sent',
                data: data.value,
                borderColor: [
                    "red",
                    "#f96332",
                    "blue",
                    "green"
                ],
                fill: true,
                backgroundColor: [
                    gradientFill,
                    gradientFill2,
                    gradientFill3,
                    gradientFill4
                ],
                borderWidth: 1,
            }]
        },
        options: {
            legend: {
                display: false
            }
        }

    });
}

function emptyCall() {

    $('#tickets_sent_body').html('<span>None tickets sent</span>')

}
