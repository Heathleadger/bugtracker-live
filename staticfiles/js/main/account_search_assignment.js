
var search_btn = document.getElementById('filter_btn')
var body = document.getElementById('table_body')

search_btn.addEventListener('click', function(e){
e.preventDefault()
var search = document.getElementById('search_bar').value
var url = 'http://127.0.0.1:8000/accounts_json/?search=' + search;
fetch(url)
.then(data => data.json())
.then(data =>{
    console.log(data)
    var table_body = `
    <input type="hidden" name="form-TOTAL_FORMS" value="${data.length}" id="id_form-TOTAL_FORMS">
    <input type="hidden" name="form-INITIAL_FORMS" value="${data.length}" id="id_form-INITIAL_FORMS">
    <input type="hidden" name="form-MIN_NUM_FORMS" value="0" id="id_form-MIN_NUM_FORMS">
    <input type="hidden" name="form-MAX_NUM_FORMS" value="1000" id="id_form-MAX_NUM_FORMS">
    `

    for (var [index,item] of data.entries()){
        table_body += `
            <input type="hidden" name="form-${index}-id" value="${item.id}" id="id_form-${index}-id">
                
            <tr>
                <td>
                ${item.id}
                </td>
                <td>${item.email} <input type="email" name="form-${index}-email" value="${item.email}" maxlength="254" hidden="" readonly="" id="id_form-${index}-email"></td>
                <td>
                <select name="form-${index}-role" class="form-control" id="id_form-${index}-role">
                <option value="1" ${item.role == 1 ? 'selected=""' :''}>Project Manager</option>

                <option value="2" ${item.role == 2 ? 'selected=""' :''}>Developer</option>

                <option value="3" ${item.role == 3 ? 'selected=""' :''}>Submiter</option>
                </select>
                </td>


            `
    }
    body.innerHTML = table_body

    })
})
