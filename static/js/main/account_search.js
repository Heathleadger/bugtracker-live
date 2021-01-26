
$(document).ready(function () {

    function listData(url) {

        console.log(url)
        fetch(url)
            .then(data => data.json())
            .then(data => {
                var table_body = ``

                for (var item of data) {
                    switch (item.role) {
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
                <tr id="stakeholder_${item.id}">
                    <td>${item.email}</td>
                    <td>${role}</td>
                    <td><button class="btn btn-primary btn_add" id="${item.id}">+</button></td>
                </tr>
                `
                }
                $('#table_body').html(table_body);

                $('.btn_add').each(function (i, obj) {
                    $(obj).click(function (e) {
                        e.preventDefault();

                        $('.added').append(`
                    <tr id="stk_added_${data[i].id}" class="mb-5">
                        <td>
                            ${data[i].email} 
                            <input type="checkbox" style="visibility: hidden; display: none;"name="stakeholder" value="${data[i].id}" checked>
                        </td>
                        <td>
                            <button class="btn btn-danger btn_remove" id="${data[i].id}">-</button>
                        </td>
                    </tr>
                    `)
                        $('#stakeholder_' + data[i].id).hide();

                        $('.btn_remove').each(function (i, obj) {
                            $(this).click(function (e) {
                                e.preventDefault();

                                var id = $(this).attr('id')
                                $('#stakeholder_' + id).show()
                                $('#stk_added_' + id).remove()

                            })
                        })
                    })

                })




            })
    }

    var url = '/api/accounts?search=';
    listData(url)

    $('#filter_btn').click(function (e) {
        e.preventDefault();

        var search = $('#search_bar').val();
        var url = '/api/accounts?search=' + search;

        listData(url)

    })





})