// DOM Elements
const addParticipantBtn = document.querySelector('#add-participant-btn');
// let participantFormContainer = document.querySelector('#participant-form-container');
let participantFormContainer = document.querySelector('#participant-form');
let i = 1;
// const visitors_count = document.querySelector('#visitors_counter');
// visitors_count.value = i;
// Add Participant Form
function addParticipantForm(event) {
    event.preventDefault();
    // document.querySelector('#submitBtn').remove();
    document.querySelector('#initial_count').innerHTML = 'Participant count : 1'
    let participantForm = document.createElement('div');
    participantForm.id = 'participant-form';
    participantForm.innerHTML = `
            <legend class="mb-0 mt-1" style="font-size: 12px;" id="initial_count">Participant count : ${i + 1}</legend>
            <div class="mb-1">
                <label for="name" class="form-label mb-0">Name:</label>
                <input type="text" class="form-control mb-1 rounded" id="name" name="name_${i}">
              </div>
              <div class="mb-1">
                <label for="address" class="form-label mb-0">Address:</label>
                <input type="text" class="form-control mb-1 rounded" id="address" name="address_${i}">
              </div>
              <div class="row">
                <div class="col">
                  <div class="mb-1">
                    <label for="age" class="form-label mb-0">Age:</label>
                    <input type="text" class="form-control mb-1 rounded" id="age" name="age_${i}" >
                  </div>
                </div>
                <div class="col">
                  <div class="mb-1">
                    <label for="pincode" class="form-label mb-0">Pin Code:</label>
                    <input type="text" class="form-control mb-1 rounded" id="pincode" name="pincode_${i}">
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <label class="mb-0" for="genter">Gender:</label>
                  <select class="form-select" id="gender" aria-label="Default select example" name="gender_${i}">
                    <option selected>Gender</option>
                    <option value="1">Male</option>
                    <option value="2">Femail</option>
                    <option value="3">Other</option>
                  </select>
                </div>
                <div class="col">
                  <label class="mb-0" for="genter">Gov Document:</label>
                  <select class="form-select" id="adhar" aria-label="Default select example" name="adhar_0">
                    <option selected>Gov Document</option>
                    <option value="1">Adhaar</option>
                    <option value="2">PAN</option>
                    <option value="3">Voter ID</option>
                  </select>
                </div>
                <div class="col">
                  <div class="mb-1">
                    <label for="adhar" class="form-label mb-0">Adhar card numeber:</label>
                    <input type="text" class="form-control mb-1 rounded" id="adhar" name="adhar_${i}">
                  </div>
                </div>
              </div>
            `;
    participantFormContainer.appendChild(participantForm);
    participantFormContainer = document.querySelector('#participant-form');
    i++;
    // visitors_count.value = i;
    if (i == 10) {
        addParticipantBtn.disabled = true;
    }
}

// Event Listeners
addParticipantBtn.addEventListener('click', addParticipantForm);
