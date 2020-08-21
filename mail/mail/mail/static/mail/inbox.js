document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
   // Send the email
  document.querySelector('form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emailread-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emailread-view').style.display = 'none';


// Load all new emails for the relevant mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    
      // Create table structure to house the mailbox title, header and emails
      document.querySelector('#emails-view').innerHTML =  `  <div>
      <h3 id="mailboxtitle"></h3>
      <table class="table table-hover table-sm">
          <thead class="thead-dark">
              <tr>
              <span id="mailboxerrormsg"></span>
              </tr>
              <tr>
                  <th scope="col">Email</th>
                  <th scope="col">Subject</th>
                  <th scope="col">Time</th>
              </tr>
          </thead>
          <tbody>
          </tbody>
      </table>
  </div>
`;
  // Show the mailbox name
  document.querySelector('#mailboxtitle').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

      emails.forEach(element => {
        const rowvar = document.createElement('tr');
        //clss = ["table-bordered" , "table-hover"]
        //rowvar.classList.add(clss);
        rowvar.id='content'; 
   // Toggle the To/From if mailbox is sent    
        if (mailbox == "sent") {
          rowvar.innerHTML = `<td>To: ${element.recipients} </td><td>Subject: ${element.subject}</td><td>Subject: ${element.timestamp}</td></tr>`;
        } 
        else {
          rowvar.innerHTML = `<td>From: ${element.sender} </td><td>Subject: ${element.subject}</td><td>Subject: ${element.timestamp}</td></tr>`;
        }
        
    // Add all the emails to the body of the table    
        document.querySelector('#emails-view > div > table > tbody').append(rowvar);
    // Add functionality to allow going to the email content when the email row is clicked
        rowvar.addEventListener('click', () => email_reader(element.id, mailbox));
    // Change row colour (by adding relevant class) depending on read status    
        readreciept = element.read;
          readreciept
          ? rowvar.classList.add("table-dark")
          : rowvar.classList.add("");
          
           })
          
        })
  
}


// Function to send the email
function send_email() {
  fetch('/emails',{
    method: 'POST',
    body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
// log the result to console to see a success/failure message
  .then(result => {
    console.log(result)
  })
// load the sent mailbox after sending the mail
.then(()=>load_mailbox("sent"));
  


  return false
}


// Function to read an email
function email_reader(emailid, mailbox) 
{
// Mark the email as read
  markread_email(emailid);
  // Show email reading view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emailread-view').style.display = 'block';

// Fetch the relevant email using the email id
  fetch(`/emails/${emailid}`)
  .then(response => response.json())
  .then(result => {
// Creating table structure
    document.querySelector('#emailread-view').innerHTML =  `  <div>
      <table class="table table-sm">
        <thead>
            <tr>
                <th scope="col">Sender:<span class="badge-pill bg-info">${result.sender}</span></th>

            </tr>
            <tr>
            <th scope="col">Recipients: ${result.recipients}</th>

        </tr>
        <tr>
        <th scope="col">Subject: ${result.subject}</th>

       </tr>
       <tr>
       <th scope="col">Sent on: ${result.timestamp}</th>

      </tr>
      
      <tr>
      <th id="archivereplybtn" scope="col"></th>
      </tr>
        </thead>
 
    </table>
    <table>
    ${result.body}
    </table>
</div>
`;
// No need for the archive/reply button in the sent mailbox
if (mailbox !== "sent") {

//Creating the archive button and attaching an event listner to it to archive the specific email using the email id
const archivebutton = document.createElement('button');
archivebutton.id = 'archivebtn';
archivebutton.innerHTML = 'Archive';
archivebutton.className = "btn btn-sm btn-outline-primary";
archivebutton.addEventListener('click', () => archive_email(result.id));

//Creating the unarchive button and attaching an event listner to it to archive the specific email using the email id
const unarchivebutton = document.createElement('button');
unarchivebutton.id = 'unarchivebtn';
unarchivebutton.innerHTML = 'Unarchive';
unarchivebutton.className = "btn btn-sm btn-outline-primary";
unarchivebutton.addEventListener('click', () => unarchive_email(result.id));

// Decide to use archive/unarchive buton depending if the email is currently archived or not
result.archived
? document.querySelector('#archivereplybtn').append(unarchivebutton)
: document.querySelector('#archivereplybtn').append(archivebutton);

//Creating the reply button and attaching an event listner to it to call the reply_email function passing the required arguments

const replybutton = document.createElement('button');
replybutton.id = 'replybtn';
replybutton.innerHTML = 'Reply';
replybutton.className = "btn btn-sm btn-outline-primary ";
replybutton.addEventListener('click', () => reply_email(result.sender, result.subject, result.timestamp, result.body));
document.querySelector('#archivereplybtn').append(replybutton);

}

  })


}

// Function to archive an email using its id
function archive_email(emailid) {
  fetch(`/emails/${emailid}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })
  .then(()=>load_mailbox("inbox"));
}

// Function to unarchive an email using its id and load the inbox after the relevant action
function unarchive_email(emailid) {
  fetch(`/emails/${emailid}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
  .then(()=>load_mailbox("inbox"));
}

// Function to mark an email as read

function markread_email(emailid) {
  fetch(`/emails/${emailid}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  
}


// Function to reply to an email
function reply_email(sender,subject,timestamp,body) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emailread-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Pre-fill the composition fields
  document.querySelector('#compose-recipients').value = sender;
  document.querySelector('#compose-body').innerHTML = `\n ${`=`.repeat(50)}= \n On ${timestamp} ${sender} wrote: \n ${body}`;
  // Check if subject already starts with Re if yes then don't add it again and if not then add Re: before the subject.
  let subj1 = subject.charAt(0)
  let subj2 = subject.charAt(1)
  subjoined = subj1 + subj2
  if (subjoined == "Re:") {
  document.querySelector('#compose-subject').value = `${subject}`;
  }
  else {
    document.querySelector('#compose-subject').value = `Re: ${subject}`;
  }

  
}