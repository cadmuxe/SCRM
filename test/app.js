/*************************************
 * Models
 ***********************************/

Customer = Em.Object.extend({
    type:null,
    manager:null,
    name:null,
    gender:null,
    birthday:null,
    memorial_days:null,
    tags:null,
    sector:null,
    vocation:null,
    phone:null,
    email:null,
    company:null,
    home_addr:null,
    


});


Project = Em.Object.extend({
    issuer:null,
    manager:null,
    project_name:null,
    working:true,
    project_sector:null,
    scale:null,
    length_project:null,
    remark:null,
    doc:null
    save:function() {
            
    }

});


