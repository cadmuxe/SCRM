(function() {
    /**************************
     * Application
     **************************/

    Crm = Ember.Application.create();

    /**************************
     * Models
     **************************/
    Crm.Customer = Ember.Object.extend({

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

    Crm.Cal = Ember.Object.extend({

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

    Crm.Memorial = Ember.Object.extend({

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

    Crm.Contract = Ember.Object.extend({

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

    Crm.Project = Ember.Object.extend({

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


    /**************************
     * Controllers and Views
     **************************/



    /**************************
     * Routers
     **************************/

    Crm.Router = Ember.Router.extend({
        location: 'hash',
        rootElement: "#",
        root:Ember.State.extend({
            index:Ember.State.extend({

                route:'/',
                redirectsTo:'inbox',
                inbox:Ember.State.extend({
                    route:'/inbox'
                }),
                today:Ember.State.extend({
                    route:'/today'
                }),
                tomorrow:Ember.State.extend({
                    route:'/tomorrow'
                })
            })

        })

    });



    $(function() {
        router = Crm.Router.create({});
        Crm.initialize(router);
    });

})();