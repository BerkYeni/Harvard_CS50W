document.addEventListener("DOMContentLoaded", function () {
  // const views = [
  //   document.querySelector("#emails-view"),
  //   document.querySelector("#compose-view"),
  //   document.querySelector("#email-view"),
  // ];

  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document
    .querySelector("#compose")
    .addEventListener("click", () => compose_email());

  // By default, load the inbox
  load_mailbox("inbox");

  const recipientsField = document.querySelector("#compose-recipients");
  const subjectField = document.querySelector("#compose-subject");
  const bodyField = document.querySelector("#compose-body");

  const composeForm = document.querySelector("#compose-form");
  composeForm.onsubmit = (event) => {
    event.preventDefault();
    const body = {
      recipients: recipientsField.value,
      subject: subjectField.value,
      body: bodyField.value,
    };

    fetch("/emails", { method: "POST", body: JSON.stringify(body) })
      .then((response) => response.json())
      .then((result) => {
        // Print result
        console.log(result);
      });

    load_mailbox("sent");
  };
});

function compose_email(recipients, subject, body) {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  const recipientsField = document.querySelector("#compose-recipients");
  const subjectField = document.querySelector("#compose-subject");
  const bodyField = document.querySelector("#compose-body");

  recipientsField.value = recipients ?? "";
  subjectField.value = subject ?? "";
  bodyField.value = body ?? "";
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  const emailsView = document.querySelector("#emails-view");
  emailsView.innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  fetch(`emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      console.log(emails);

      const emailElements = emails.map((email) => {
        const emailElement = document.createElement("li");
        if (email.read) {
          emailElement.classList.add("read");
        }
        // emailElement.onclick = (event) => {};

        const emailSubject = document.createElement("strong");
        emailSubject.classList.add("emailSubjectOverview");
        emailSubject.textContent = email.subject;
        emailSubject.onclick = (event) => {
          view_email(email.id, mailbox);
        };

        const emailSender = document.createElement("div");
        emailSender.textContent = email.sender;

        const emailDate = document.createElement("div");
        emailDate.classList.add("emailDateOverview");
        emailDate.textContent = email.timestamp;

        const emailWrapper = document.createElement("div");
        emailWrapper.classList.add("emailOverview");
        emailWrapper.append(emailSubject, emailSender, emailDate);

        emailElement.append(emailWrapper);

        return emailElement;
      });
      emailsView.append(...emailElements);
    });
}

function view_email(id, emailType) {
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  const archiveButtton = document.querySelector("#archive");
  archiveButtton.style.display = emailType === "sent" ? "none" : "inline-block";
  archiveButtton.textContent =
    emailType === "archive" ? "Un-Archive" : "Archive";

  const replyButton = document.querySelector("#reply");
  replyButton.style.display = emailType === "sent" ? "none" : "inline-block";

  fetch(`emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      console.log(email);
      document.querySelector("#from").textContent = email.sender;
      document.querySelector("#to").textContent = email.recipients.join(", ");
      document.querySelector("#subject").textContent = email.subject;
      document.querySelector("#timestamp").textContent = email.timestamp;
      document.querySelector("#body").textContent = email.body;

      archiveButtton.onclick = (event) => {
        fetch(`emails/${id}`, {
          method: "PUT",
          body: JSON.stringify({
            archived: email.archived ? false : true,
          }),
        });
        load_mailbox("inbox");
      };

      replyButton.onclick = (event) => {
        const subject = email.subject.startsWith("Re: ")
          ? email.subject
          : `Re: ${email.subject}`;
        const splitByQuotes = email.body.split('"');
        const replyToReply =
          splitByQuotes.length > 1
            ? splitByQuotes[0].endsWith("wrote: \n")
            : false;
        const body = `On ${email.timestamp} ${email.sender} wrote: \n"${
          !replyToReply ? email.body : splitByQuotes.slice(2).join('"').trim()
        }"`;
        compose_email(email.sender, subject, body);
      };

      fetch(`emails/${id}`, {
        method: "PUT",
        body: JSON.stringify({ read: true }),
      });
    });
}
