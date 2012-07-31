/*************************************
 * Models
 ***********************************/

Customer = Em.Object.extend({

    save: function() {
        console.log(JSON.stringify(this));
        var request = $.ajax({
            type: "POST",
            url: "/api/customer/save",
            contentType:"application/json",
            data: JSON.stringify(this),
            success: function(data) {
                return true;
            }
        });
        return 'ok';
    }

});

Cal = Em.Object.extend({

    save: function() {
        console.log(JSON.stringify(this));
        var request = $.ajax({
            type: "POST",
            url: "/api/cal/save",
            contentType:"application/json",
            data: JSON.stringify(this),
            success: function(data) {
                return true;
            }
        });
        return 'ok';
    }

});

Memorial = Em.Object.extend({

    save: function() {
        console.log(JSON.stringify(this));
        var request = $.ajax({
            type: "POST",
            url: "/api/memorial/save",
            contentType:"application/json",
            data: JSON.stringify(this),
            success: function(data) {
                return true;
            }
        });
        return 'ok';
    }

});

Contract = Em.Object.extend({

    save: function() {
        console.log(JSON.stringify(this));
        var request = $.ajax({
            type: "POST",
            url: "/api/contract/save",
            contentType:"application/json",
            data: JSON.stringify(this),
            success: function(data) {
                return true;
            }
        });
        return 'ok';
    }

});

Project = Em.Object.extend({

    save: function() {
        console.log(JSON.stringify(this));
        var request = $.ajax({
            type: "POST",
            url: "/api/project/save",
            contentType:"application/json",
            data: JSON.stringify(this),
            success: function(data) {
                return true;
            }
        });
        return 'ok';
    }

});


