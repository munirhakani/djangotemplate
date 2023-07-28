;(function () {
    
    const modal = new bootstrap.Modal(document.getElementById("modal"))

    htmx.on("htmx:afterSwap", (e) => {
        if (e.detail.target.id == "dialog") {
            modal.show();
        }
    })
    
    htmx.on("htmx:beforeSwap", (e) => {
        if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
            modal.hide();
            e.detail.shouldSwap = false;
        }
    })

    htmx.on("error", (e) => {
        alert(e.detail.value);
    })

    htmx.on("create_pk", (e) => {
        htmx.ajax('GET', 'object/'+e.detail.value+'/', {
            target:'#target', swap:'outerHTML', values: {'create': true, },
        });
        modal.hide();
	})

    htmx.on("update_pk", (e) => {
        htmx.ajax('GET', 'object/'+e.detail.value+'/', {
            target:'#object-' + e.detail.value, swap:'outerHTML',
        });
        modal.hide();
	})

    htmx.on("shown.bs.modal", (e) => {
        $('#formModal').find('input[type=text],textarea,select').filter(':visible:first').focus();
        $('#formModal').find('input[type=text],textarea,select').filter(':visible:first').select();
    })

    htmx.on("delete_pk", (e) => {
        $('#object-' + e.detail.value).replaceWith('<tr></tr>');
        modal.hide();
	})

    htmx.on("hidden.bs.modal", () => {
        document.getElementById("dialog").innerHTML = "";
    })
})()