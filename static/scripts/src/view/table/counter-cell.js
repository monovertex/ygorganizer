

define([
    'underscore',
    'backgrid',
    'templates'
], function (_, Backgrid, Templates) {

    return Backgrid.IntegerCell.extend({

        className: 'counter-cell',

        events: {
            'click .decrease': 'decrease',
            'click .increase': 'increase'
        },

        template: Templates.counter,

        initialize: function (options) {
            Backgrid.IntegerCell.prototype.initialize.apply(this, arguments);

            _.bindAll(this, 'render');

            this.countClass = options.column.get('countClass') ||
                'text-primary';

            this.listenTo(
                this.model,
                'change@' +
                    _.initial(this.column.get('name').split('.')).join('.'),
                this.render
            );
        },

        render: function () {
            Backgrid.IntegerCell.prototype.render.apply(this, arguments);

            var count = this.$el.text();

            this.$el.html(this.template()).find('.count')
                .addClass(this.countClass).text(count);

            if (count === '0') {
                this.$el.removeClass('non-zero').addClass('zero');
            } else {
                this.$el.addClass('non-zero').removeClass('zero');
            }

            return this;
        },

        update: function (count) {
            if (count < 0) {
                count = 0;
            }

            this.model.set(this.column.get('name'), count,
                { 'updateCount': true });
            this.render();
        },

        decrease: function () {
            this.update(this.model.get(this.column.get('name')) - 1);
        },

        increase: function () {
            this.update(this.model.get(this.column.get('name')) + 1);
        }

    });

});