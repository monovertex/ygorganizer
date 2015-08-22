module.exports = function (grunt) {

    var debug = false;

    grunt.initConfig({

        folders: {
            scripts: {
                base: 'static/scripts/',
                src: 'static/scripts/src/',
                lib: 'static/scripts/lib/'
            },
            styles: {
                base: 'static/styles/',
                src: 'static/styles/src/',
                lib: 'static/styles/lib/'
            },
            templates: {
                base: 'static/templates/',
                src: 'static/templates/src/'
            }
        },

        pkg: grunt.file.readJSON('package.json'),

        jshint: {
            files: [
                'Gruntfile.js',
                '<%=folders.scripts.src %>**/*.js'
            ],
            options: {
                globals: {
                    console: true,
                    document: true
                },
                debug: debug
            }
        },

        requirejs: {
            compile: {
                options: {
                    baseUrl: '<%=folders.scripts.lib %>',

                    mainConfigFile: '<%=folders.scripts.src %>main.js',

                    name: 'app/initialize',

                    insertRequire: ['app/initialize'],

                    out: '<%=folders.scripts.base %>build.js',

                    include: ['almond'],

                    optimize: 'uglify2',

                    shim: {
                        'nouislider': ['jquery']
                    },

                    wrapShim: true,

                    done: function (done, output) {
                        grunt.log.writeln(output);
                        done();
                    }
                }
            }
        },

        jst: {
            compile: {
                options: {
                    amd: true,
                    namespace: 'JST',
                    processName: function (filename) {
                        return filename
                            .replace('static/templates/src/', '')
                            .replace('.html', '');
                    },
                },
                files: {
                    '<%=folders.templates.base %>build.js':
                        ['<%=folders.templates.src %>**/*.html']
                }
            }
        },

        less: {
            compile: {
                options: {
                    strictMath: true,
                    paths: [
                        '<%=folders.styles.src %>',
                        '<%=folders.styles.lib %>'
                    ]
                },
                files: {
                    '<%=folders.styles.base %>build.css':
                        '<%=folders.styles.src %>main.less'
                }
            }
        },

        autoprefixer: {
            options: {
                browsers: [
                    'Android 2.3',
                    'Android >= 4',
                    'Chrome >= 20',
                    'Firefox >= 24',
                    'Explorer >= 8',
                    'iOS >= 6',
                    'Opera >= 12',
                    'Safari >= 6'
                ]
            },
            core: {
                src: '<%=folders.styles.base %>build.css'
            }
        },

        cssmin: {
            options: {
                compatibility: 'ie8',
                noAdvanced: true
            },
            core: {
                files: {
                    '<%=folders.styles.base %>build.css':
                        '<%=folders.styles.base %>build.css'
                }
            }
        },

        watch: {
            templates: {
                files: [
                    'Gruntfile.js',
                    '<%=folders.templates.src %>**/*.html'
                ],
                tasks: ['templates']
            },
            js: {
                files: [
                    'Gruntfile.js',
                    '<%=folders.templates.base %>build.js',
                    '<%=folders.scripts.src %>**/*.js',
                    '<%=folders.scripts.lib %>**/*.js'
                ],
                tasks: ['scripts']
            },
            less: {
                files: [
                    'Gruntfile.js',
                    '<%=folders.styles.src %>**/*.less',
                    '<%=folders.styles.lib %>**/*.less'
                ],
                tasks: ['styles']
            }
        },
    });

    require('load-grunt-tasks')(grunt);

    if (debug) {
        grunt.registerTask('styles', ['less']);
    } else {
        grunt.registerTask('styles', ['less', 'autoprefixer', 'cssmin']);
    }

    if (debug) {
        grunt.registerTask('scripts', ['jshint']);
    } else {
        grunt.registerTask('scripts', ['jshint', 'requirejs']);
    }

    grunt.registerTask('templates', ['jst']);

    grunt.registerTask('default', ['templates', 'scripts', 'styles']);

};