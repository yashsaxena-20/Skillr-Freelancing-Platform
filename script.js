async function loadJobs(){

let res = await fetch('/jobs')
let jobs = await res.json()

let table = document.getElementById("jobsTable")

table.innerHTML = `
<tr>
<th>Job ID</th>
<th>Title</th>
<th>Base Price</th>
<th>Status</th>
</tr>
`

jobs.forEach(job=>{

table.innerHTML += `
<tr>
<td>${job.job_id}</td>
<td>${job.title}</td>
<td>${job.base_price}</td>
<td>${job.job_status}</td>
</tr>
`
})
}



async function placeBid(){

let res = await fetch('/bids',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({
job_id:document.getElementById("job_id").value,
freelancer_id:document.getElementById("freelancer_id").value,
price:document.getElementById("price").value
})
})

let data = await res.json()

if(data.error){
alert(data.error)
}else{
alert(data.message)
}

}



async function createContract(){

let res = await fetch('/contracts',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({
job_id:document.getElementById("c_job").value,
freelancer_id:document.getElementById("c_freelancer").value,
start_date:document.getElementById("c_date").value,
price:document.getElementById("c_price").value
})
})

let data = await res.json()

if(data.error){
alert(data.error)
}else{
alert(data.message)
}

}



async function makePayment(){

let res = await fetch('/payment',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({
contract_id:document.getElementById("contract_id").value,
amount:document.getElementById("amount").value,
type:document.getElementById("ptype").value,
status:document.getElementById("pstatus").value
})
})

let data = await res.json()

if(data.error){
alert(data.error)
}else{
alert(data.message)
}

}

async function submitReview(){
let res = await fetch('/review',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({
contract_id:document.getElementById("r_contract").value,
reviewer:document.getElementById("reviewer").value,
reviewee:document.getElementById("reviewee").value,
rating:document.getElementById("rating").value,
comment:document.getElementById("comment").value
})
})

let data = await res.json()
if(data.error){
alert(data.error)
}else{
alert(data.message)
}

}

async function txRead(){
let res = await fetch('/tx_read',{method:'POST'})
let data = await res.json()
tx_output.innerText = data.error || data.message
}

async function txSafe(){
let res = await fetch('/tx_update_safe',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({job_id:safe_job.value})
})
let data = await res.json()
tx_output.innerText = data.error || data.message
}

async function txConflict(){
let res = await fetch('/tx_conflict',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({
job_id:conflict_job.value,
delay:conflict_delay.value
})
})
let data = await res.json()
tx_output.innerText = data.error || data.message
}

async function txDeadlock(){
let res = await fetch('/tx_deadlock',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({
job1:d_job1.value,
job2:d_job2.value,
delay:d_delay.value
})
})
let data = await res.json()
tx_output.innerText = data.error || data.message
}

async function txDirty(){
let res = await fetch('/tx_dirty',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({job_id:dirty_job.value})
})
let data = await res.json()
tx_output.innerText = data.error || data.message
}
async function txDirtyWrite(){
let res = await fetch('/tx_dirty_write',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({job_id:dirty_job.value})
})
let data = await res.json()
tx_output.innerText = data.error || data.message
}