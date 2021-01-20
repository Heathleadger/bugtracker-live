$('#filter_btn').click(function(e){
    e.preventDefault();

    var search = $('#search_bar').val();
    console.log(search)
    var url = 'http://127.0.0.1:8000/accounts_json/?search=' + search;

    fetch(url)
    .then(data => data.json())
    .then(data =>{
        console.log(data)
        var table_body = ``

        for (var item of data){
            switch (item.role){
                case 1: 
                    var role = "Project Manager";
                    break;
                case 2:
                    var role = "Developer";
                    break;
                default:
                    var role = "Submiter";
            }
            table_body += `
            <tr>
                <td>${item.email}</td>
                <td>${role}</td>
                <td><button class="btn btn-primary">Add</button></td>
            </tr>
            `
        }
        body.innerHTML = table_body;

})
