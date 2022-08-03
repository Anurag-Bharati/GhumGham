$('.delete-log > button').on('click', function (e) {
    e.preventDefault();
    let form = $(this).parents('form');
    swal({
        title: "Are you sure?",
        text: "Once deleted, you will not be able to recover this log!",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                form.submit();
            } else {
                swal("Cancelled", "The log is safe :)", {
                    icon: "info",
                });
            }
        });
});

$('.unban-user > button').on('click', function (e) {
    e.preventDefault();
    let form = $(this).parents('form');
    swal({
        title: "Unban this user?",
        text: "You can ban the user at anytime",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                form.submit();
            } else {
                swal("Cancelled", "Noting changed :)", {
                    icon: "info",
                });
            }
        });
});

$('.ban-user > button').on('click', function (e) {
    e.preventDefault();
    let form = $(this).parents('form');
    swal({
        title: "Ban this user?",
        text: "You can unban the user at anytime",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                form.submit();
            } else {
                swal("Cancelled", "Noting changed :)", {
                    icon: "info",
                });
            }
        });
});