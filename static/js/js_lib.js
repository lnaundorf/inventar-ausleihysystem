function filter_search(name) {
	if(name.substr(0,6) == "schein") {
		div = "#tablediv_" + name.substr(7);
		id = '#filter_' + name.substr(7);
	} else {
		div = "#tablediv";
		id = '#filter';
	}
	
	$.get("/" + name + "/filter/?s=" + escape($(id).val()), function(data) {
		$(div + ' table tbody').html(data);
		var table = $(div + ' table');
		table.trigger('update', [true]);
	});
}

function addItem(id) {
	$.get('/inventar/add/?id=' + id, function(data) {
		if (data == "error") {
			alert("error");
		} else {
			$('#erstelllink').html('erstellen');
			$('#scheinul').append(data);
			filter_search("inventar");
		}
	});
}

function removeItem(id) {
	$.get('/inventar/remove/?id=' + id, function(data){
		if (data == "error") {
			alert("error");
		} else {
			$('#schein' + id).remove();
			if($('#scheinul').children().length == 0){
				$('#erstelllink').html('');
			}
			if($('#inventarsuche')) {
				filter_search("inventar");
			}
		}
	});
}

function getUser(id) {
	resetDownload();
	$.get("/benutzer/getUser/?id=" + id, function(data) {
		if (data == "error") {
			alert("error");
		} else {
			$('#UserInfo').html(data);
		}
	});
}

function download() {
	user = $("#benutzer").val();
	begindate = $("#dp1").val();
	enddate = $("#dp2").val();
	abholer = $("#abholer:checked").length;

	window.open("/schein/download/?u=" + user + "&begindate=" + escape(begindate) + "&enddate=" + escape(enddate) + "&abholer=" + abholer, "schein");
	$("#download").html('<a href="/schein/issue/" class="btn btn-primary">Schein ausstellen</a>');
}

function resetDownload() {
	$("#download").html("");
}

function newType() {
	name = $("#typeName").val();
	if (name != "") {
		$.get("/inventar/addType/?name=" + escape(name), function(data) {
			if(data == "ERROR") {
				alert("error");
			} else {
				$('#id_typ').append(new Option(name, data, false, true));
				$('#modal').modal('hide');
				$("#typeName").val("");
			}
		});
	}
}
