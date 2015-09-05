module.exports = function (grunt) {

    grunt.initConfig({

        folders: {
            scripts: {
                base: 'static/scripts/',
                src: '<%= folders.scripts.base %>src/',
                lib: '<%= folders.scripts.base %>lib/'
            },
            styles: {
                base: 'static/styles/',
                src: '<%= folders.styles.base %>src/',
                lib: '<%= folders.styles.base %>lib/'
            },
            templates: {
                base: 'static/templates/',
                src: '<%= folders.templates.base %>src/'
            }
        },

        pkg: grunt.file.readJSON('package.json'),

        jshint: {
            options: {
                globals: {
                    console: true,
                    document: true
                },
            },
            prod: {
                options: {
                    debug: false
                },
                src: [
                    'Gruntfile.js',
                    '<%= folders.scripts.src %>**/*.js'
                ],
            },
            dev: {
                options: {
                    debug: true
                },
                src: '<%= jshint.prod.src %>'
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
                advanced: false,
                aggressiveMerging: false,
                restructuring: false,
                roundingPrecision: -1,
                shorthandCompacting: false,
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

    grunt.registerTask('styles', ['less']);

    grunt.registerTask('scripts', ['jshint:dev']);

    grunt.registerTask('templates', ['jst']);

    grunt.registerTask('default', ['templates', 'scripts', 'styles']);

    grunt.registerTask('prod', [
        'jst', 'jshint:prod', 'requirejs',
        'less', 'autoprefixer', 'cssmin'
    ]);

};