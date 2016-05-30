'use strict';

/**
 * @ngdoc function
 * @name inAppTranlsationApp.controller:AppviewCtrl
 * @description
 * # AppviewCtrl
 * Controller of the inAppTranlsationApp
 */
angular.module('inAppTranlsationApp')
  .controller('AppviewCtrl', function ($scope, $routeParams, App, _, $http, config, Translation, Word, FileReader, $rootScope) {
    $scope.size_options = [
      {'value': 20, 'text': 20},
      {'value': 40, 'text': 40},
      {'value': 60, 'text': 60},
      {'value': 80, 'text': 80},
      {'value': 100, 'text': 100}
    ];
    function _get_row_style() {
      return {'width': (($scope.data.langs.length+1)*370+150)+'px'};
    }
    $scope.scrollTop = 0;
    $rootScope.loading = true;
    $scope.import_step1 = false;
    $scope.push_popup = false;
    $scope.app = App.get({id: $routeParams.id});
    $scope.new_word = '';
    function getAvailLangs() {
      var temp = [];
      for (var i in $scope.data.langs) {
        temp.push($scope.data.langs[i]);
      }
      var keys = _.difference(_.keys(window.langData), temp);
      var avail_langs = [];
      for (var i in keys) {
        avail_langs.push({val: keys[i], caption: window.langData[keys[i]]});
      }
      return avail_langs;
    }


    App.localwords({id: $routeParams.id, custom: '/localwords'}).$promise.then(function(data) {
      $scope.data = data;
      $scope.row_width = _get_row_style();
      $scope.avail_langs =  getAvailLangs();
      $rootScope.loading = false;
      $scope.$broadcast('dataloaded');
    });

    $scope.langData = window.langData;

    $scope.addLang = function(lang) {
      $scope.data.langs.push(lang);
      $scope.row_width = _get_row_style();
      $scope.avail_langs = _.reject($scope.avail_langs, function(item) { return  lang == item.val; });
    };

    $scope.removeLang = function(index) {
      window.alertify.confirm('Do you really want to delete this Language?', function(e) {
        if (e) {
          var deleted_lang = $scope.data.langs[index];
          $scope.data.langs.splice(index, 1);
          $scope.row_width = _get_row_style();
          $scope.avail_langs = getAvailLangs();
          var url = config.api_url+'/apps/'+$scope.app.id+'/lang?code='+deleted_lang;
          $http.delete(url);
        }
      });
    };

    $scope.updateKey = function($child_scope) {
      var url = config.api_url + '/words/'+$child_scope.word.id;
      $http.put(url, {id: $child_scope.word.id, app: $child_scope.word.app, name: $child_scope.updated_key}).success(function() {
        $child_scope.word.name = $child_scope.updated_key;
        $child_scope.$hide();
      })
    };

    $scope.deleteKey = function($child_scope) {
      var url = config.api_url + '/words/'+$child_scope.word.id;
      $http.delete(url).success(function() {
        $scope.reload();
      });
    };

    $scope.addTranslation = function($child_scope) {
      Translation.save({
        name: $child_scope.local_word,
        lang: $child_scope.lang,
        word: $child_scope.word.id,
        app: $scope.app.id
      }, function(data) {
        if (!$scope.data.translations[data.word]) {
          $scope.data.translations[data.word] = {};
        }
        if (!$scope.data.translations[data.word][$child_scope.lang]) {
          $scope.data.translations[data.word][$child_scope.lang] = {};
        }
        $scope.data.translations[data.word][$child_scope.lang] = data;
      });
    };

    $scope.selectTranslation = function($cscope, item) {
      if (item.selected) {
        return;
      }
      item.selected = true;
      Translation.update(item);
      for (var i in $scope.data.translations[$cscope.word.id][$cscope.lang]) {
        if ($scope.data.translations[$cscope.word.id][$cscope.lang][i].id != item.id) {
          $scope.data.translations[$cscope.word.id][$cscope.lang][i].selected = false;
        }
      }

    };

    $scope.removeTranslation = function($cscope, item, index) {
      window.alertify.confirm('Do you really remove this translation?', function(e) {
        if (e) {
          Translation.delete({
            id: item.id
          }, function(data) {
            if (data.id != -1) {
              for (var i in $scope.data.translations[$cscope.word.id][$cscope.lang]) {
                if ($scope.data.translations[$cscope.word.id][$cscope.lang][i].id == data.id) {
                  $scope.data.translations[$cscope.word.id][$cscope.lang][i].selected = true;
                }
              }
            }
          });
          $scope.data.translations[$cscope.word.id][$cscope.lang].splice(index, 1);
        }
      });
    };

    $scope.addWord = function($cscope, close) {
      $rootScope.loading = true;
      Word.save({app: $scope.app.id, name: $cscope.new_word}, function(data) {
        $scope.data.words.unshift(data);
        $scope.data.end_index++;
        if (close) {
          $cscope.$hide();
        }
        $cscope.new_word = '';
        $rootScope.loading = false;
      }, function(data) {
        if (data.status == 400) {
          $rootScope.loading = false;
          $cscope.new_word = '';
          window.alertify.error('Duplicated word')
        }
      }
      );
    };

    $scope._geExportValue = function(val) {
      var _l = val.replace(/\\/g, '\\\\');
      _l = _l.replace(/'/g, "\\'");
      _l = _l.replace(/"/g, '\\"');
      _l = _l.replace(/%@/g, '%s');
      _l = _l.replace(/\$@/g, '$s');
      _l = _l.replace('&', '&amp;');
      _l = _l.replace('>', '&gt;');
      _l = _l.replace('<', '&lt;');

      return _l;
    };

    $scope.export = function(env) {
      $rootScope.loading = true;
      $scope.show_export = false;
      var zip = new window.JSZip();
      var url = config.api_url + '/apps/'+$routeParams.id+'/web_translations';
      $http.get(url, {})
        .success(function(data) {
          var translations = data.translations;
          if (!translations.length) {
            $rootScope.loading = false;
            window.alertify.alert("You don't have translation data to export yet.");
            return;
          }
          var _len = translations.length;
          if (env == 'android') {
            _len += 1;
          }
          var cb = _.after(_len, function () {
            var content = '';
            if (window.bowser.safari) {
              window.alertify.alert('In Safari, eported file will be named as "Unkown" (without zip extension). But this is a zip file. Please double click this "Unknown" file to unzip the file');
              content = zip.generate();
              window.location.href = "data:application/zip;base64," + content;
            } else {
              content = zip.generate({type: "blob"});
              window.saveAs(content, $scope.app.name + ".zip");
            }
            //$('.export-btn').attr('download', self.curApp.get("name") + ".zip");
            $rootScope.loading = false;

          });
          var keys = [];
          _.each(translations, function (data) {
            if (env == 'ios') {

              var folder = zip.folder(data.lang + ".lproj");

              var exportStr = "/*\n";
              exportStr += ( "Localizable.strings\n");
              exportStr += ( window.langData[data.lang] + " words for '" + $scope.app.name + "'\n");
              exportStr += ( "Created by InAppTranslation on " + (new Date().toString('M/d/yyyy')) + "\n" );
              exportStr += "*/\n\n\n";
              for (var _i in data.content) {
                var val = data.content[_i].translation;
                var _w = data.content[_i].word.replace(/"/g, '\\"');
                var _l = val.replace(/\\/g, '\\\\');
                _l = _l.replace(/"/g, '\\"');
                exportStr += ('"' + _w + '" = "' + _l + '";\n');
              }

              folder.file("Localizable.strings", window.Base64.encode(exportStr), {base64: true});
            } else {
              var lang = data.lang;
              if (lang == 'zh-Hans') {
                lang = 'zh-CN';
              }
              if (lang == 'zh-Hant') {
                lang = 'zh-TW';
              }
              var temp = lang.split('-');
              if (temp.length > 1) {
                temp[1] = 'r' + temp[1];
              }
              var folderName = 'values';
              for(var i in temp) {
                folderName += ('-' + temp[i]);
              }

              var folder = zip.folder(folderName);
              var exportStr = '<?xml version="1.0" encoding="utf-8"?>';
              exportStr += "<!--\n";
              exportStr += ( "Localizable.strings\n");
              exportStr += ( window.langData[data.lang] + " words for '" + $scope.app.name + "'\n");
              exportStr += ( "Created by InAppTranslation on " + (new Date().toString('M/d/yyyy')) + "\n" );
              exportStr += "-->\n\n";
              exportStr += "<resources>\n";
              var _keys = [];
              for (var _i in data.content) {
                var val = data.content[_i].translation;
                var key = data.content[_i].word;
                var _w = key.replace(/"/gmi, '');
                _w = _w.replace(/'/g, '');
                _w = _w.replace(/[\.\-/ ]/gmi, '_');
                _w = _w.replace(/[^a-z0-9_]/gmi, 'x');
                if ('0' <= _w[0] && _w[0] <= '9') {
                  _w = '_' + _w;
                }
                _w = _w.substring(0, Math.min(100, _w.length));
                if (!_.findWhere(_keys, {key: _w, val: val})) {
                  _keys.push({key: _w, val: val});
                } else {
                  var __w = _w.substring(0, Math.min(99, _w.length));
                  var index = 1;
                  while(_.findWhere(_keys, {key: __w+index, val: val})) {
                    index += 1;
                  }
                }
                if (!_.findWhere(keys, {key: _w})) {
                  keys.push({key: _w, val: $scope._geExportValue(key)});
                }

                var _l = $scope._geExportValue(val);
                var count = (_l.match(/%/gmi) || []).length;
                exportStr += ('\t<string name="'+_w+'"'+(count > 1 ? ' formatted="false"' : '')+'>'+_l+'</string>\n');
              }
              exportStr += "</resources>";
              folder.file("strings.xml", window.Base64.encode(exportStr), {base64: true});
            }
            cb();
          });

          if (env == 'android') {
            var folder = zip.folder('values');
            var exportStr = '<?xml version="1.0" encoding="utf-8"?>';
            exportStr += "<!--\n";
            exportStr += ( "Localizable.strings\n");
            exportStr += ( "Base words for '" + $scope.app.name + "'\n");
            exportStr += ( "Created by InAppTranslation on " + (new Date().toString('M/d/yyyy')) + "\n" );
            exportStr += "-->\n\n";
            exportStr += "<resources>\n";

            for (var i in keys) {
              var _w = keys[i].key;
              var _l = keys[i].val;
              var count = (_l.match(/%/gmi) || []).length;
              exportStr += ('\t<string name="'+_w+'"'+(count > 1 ? ' formatted="false"' : '')+'>'+_l+'</string>\n');
            }
            exportStr += "</resources>";
            folder.file("strings.xml", window.Base64.encode(exportStr), {base64: true});
            cb();
          }
        })
        .error(function(data) {
          window.alertify.error(data['errors']);
          $rootScope.loading = false;
        });
    };

    $scope.import_next = function() {

      if (!this.import_lang) {
        window.alertify.alert("Please select a language.");
      } else {
        $scope.selected_lang = this.import_lang;
        $scope.import_step1 = false;
        $scope.import_step2 = true;
      }
    };
    $scope.upload = function(file) {
      FileReader.readAsText(file[0], 'utf-8', $scope)
        .then(function (rest) {
          //console.log(rest);
          var str = rest;
          str = str.trim();
          str = str.replace(/^\s*\/\/.+$/mg, "");
          str = str.replace(/\/\*(.|\n)*?\*\//g, "");
          str = str.replace('\\“', '\\"');
          str = str.replace('\\”', '\\"');
          var lines = str.split('";');
          var success = 0, failed = 0, repeat = 0,  _json = [];
          var failed_str = [];
          for (var i=0; i< lines.length; i++) {
            if (lines[i] && lines[i].length > 0) {
              var line = lines[i];
              line = line.replace(/^\s*\/\/.+$/mg, "");
              line = line.trim();
              if (!line) {
                continue;
              }
              line = line.replace(/"\s=\s"/g, "\":\"");
              line = line.replace(/;/g, "");
              line = "{" + line + "\"}";
              try {
                var json = window.jQuery.parseJSON(line);
                success += 1;
                _json.push(json);
              } catch(e) {
                failed_str.push((lines[i]+"\";"));
                failed += 1;
              }
            }
          }

          function doImport() {
            if (_json !== null) {
              var url = config.api_url + '/translations/import_localwords';
              var temp = [];
              var all_words = [];
              for (var i=0; i<_json.length;i++) {
                for (var k in _json[i]) {
                  if (all_words.indexOf(k) === -1) {
                    temp.push({word: k, val: _json[i][k]});
                    all_words.push(k);
                  } else {
                    success -= 1;
                    console.log(k);
                  }
                }
              }
              var data = {data: temp};
              data.app = $routeParams.id;
              data.lang = $scope.selected_lang;
              data.pz = $scope.data.page_size;
              $rootScope.loading = true;
              $scope.import_step2 = false;
              $http.post(url, data)
                .success(function (data) {
                  $scope.data = data;
                  $scope.avail_langs = getAvailLangs();
                  $scope.row_width = _get_row_style();
                  $rootScope.loading = false;
                  if (success > 0) {
                    window.alertify.success(success+" translation" +(success > 1 ? 's' : '') + " are imported.");
                  }
                  if (failed > 0) {
                    window.alertify.error(failed+" translation" +(failed > 1 ? 's' : '') + " are failed");
                  }
                })
                .error(function () {
                  $rootScope.loading = false;
                  window.alertify.error("There was an error while process import on server side.");
                });
            }
          }
          if (failed > 0) {
            alertify.set({ labels: {
              ok     : "See Errors",
              cancel : "Continue"
            } });
            window.alertify.confirm("We found "+failed + " invalid translation"+(failed > 1 ? 's' : '')+'. Would you like continue or see invalid translations?', function(e) {
              alertify.set({ labels: {
                ok     : "OK",
                cancel : "Cancel"
              }});
              if (e) {
                console.log(failed_str);
                window.alertify.alert("Invalid translations...<br>"+failed_str.join("<br>"));
              } else {
                doImport();
              }
            });
          } else {
            doImport();
          }


        });
    };

    $scope.send_push = function(type) {
      var url = config.api_url + '/apps/'+$scope.app.id+'/send_push?type='+type;
      $rootScope.loading = true;
      $http.get(url, {})
        .success(function(data) {
          $scope.push_popup = false;
          $rootScope.loading = false;
          window.alertify.success('Sending push notification is being done on server side.')
        })
        .error(function(data) {
          $scope.push_popup = false;
          window.alertify.error(data['errors']);
          $rootScope.loading = false;
        });
    };

    $scope.load_next_page = function() {
      $scope.data.page ++;
      $scope.reload();
    };

    $scope.load_prev_page = function() {
      $scope.data.page --;
      $scope.reload();
    };

    $scope.reload = function() {
      var url = config.api_url + '/apps/'+$routeParams.id+'/localwords?p='+$scope.data.page+'&pz='+$scope.data.page_size;
      $rootScope.loading = true;
      $http.get(url).success(function(data) {
        $scope.data = data;
        $scope.row_width = _get_row_style();
        $scope.avail_langs =  getAvailLangs();
        $rootScope.loading = false;
        $scope.$broadcast('dataloaded');
      });
    };

  });
