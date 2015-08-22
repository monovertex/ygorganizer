

define([
    'underscore',
    'backbone',
    'backbone.relational'
], function (_, Backbone) {

    return Backbone.RelationalModel.extend({

        url: '/api/user-card/',

        initialize: function () {
            _.bindAll(this, 'save', 'prepareSave', 'afterSave');

            this.listenTo(this, 'change', this.prepareSave);
        },

        prepareSave: function (model, options) {
            if (options.updateCount) {
                if (this.saveDelay) {
                    window.clearTimeout(this.saveDelay);
                    delete this.saveDelay;
                }

                this.saveDelay = window.setTimeout(this.save, 500);
            }
        },

        save: function () {
            Backbone.RelationalModel.prototype.save.apply(this, arguments)
                .done(this.afterSave);
        },

        afterSave: function () {
            this.trigger('updateCount');
        }

    });

});