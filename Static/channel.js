document.addEventListener('DOMContentLoaded', () => {

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  socket.on('connect', () => {
    socket.emit('joined');
    document.querySelector('#form').onsubmit = () => {
      var message = document.querySelector("#message").value;
      if (document.querySelector("#broadcast").value == "worldwide") {
      socket.emit('submit worldwide post', {'message': message});
      } else {
      socket.emit('submit post', {'message': message});
      };
      document.querySelector("#message").value = '';
      return false;
    };
    document.querySelector('#delete').onclick = () => {
      if (confirm("Are you sure you want to delete this channel?")) {
        socket.emit('delete channel');
      } else {
        console.log("delete canceled");
      };
    };
    window.onbeforeunload = () => {
      socket.emit('left');
    }
  });

  socket.on('announce post', data => {
    var li = document.createElement('li');
    li.innerHTML = `<strong> ${data.username} </strong> : ${data.message} <small class="float-right"> ${data.time} </small>`;
    document.querySelector('#posts').append(li);
  });

  socket.on('announce post worldwide', data => {
    var li = document.createElement('li');
    li.innerHTML = `<strong> admin </strong> : ${data.message} <small class="float-right"> ${data.time} </small>`;
    document.querySelector('#posts').append(li);
  });

  socket.on('status', data => {
    var div = document.createElement('div');
    div.innerHTML = `---${data.msg}---`;
    document.querySelector('#posts').append(div);
  });

  socket.on('redirect', data => {
    window.location = data.url;
  });
});
