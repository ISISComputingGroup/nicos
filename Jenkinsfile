#!groovy

//*** job setup */
properties([
    buildDiscarder(logRotator(artifactDaysToKeepStr: '',
                              artifactNumToKeepStr: '',
                              daysToKeepStr: '',
                              numToKeepStr: '50')),
    parameters([
        string(defaultValue: 'frm2/nicos/nicos-core',
               description: '', name: 'GERRIT_PROJECT'),
        string(defaultValue: 'refs/heads/master',
               description: '', name: 'GERRIT_BRANCH'),
        string(defaultValue: 'refs/heads/master',
               description: '', name: 'GERRIT_REFSPEC'),
        choice(choices: '''\
patchset-created
ref-updated
change-merged''',
        description: '', name: 'GERRIT_EVENT'),
        choice(choices: '''\
patchset-created
ref-updated
change-merged''',
        description: '', name: 'GERRIT_EVENT_TYPE')]),
        [$class: 'ScannerJobProperty', doNotScan: false],
        [$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false],
        [$class: 'ThrottleJobProperty', categories: [],
            limitOneJobWithMatchingParams: false,
            maxConcurrentPerNode: 0,
            maxConcurrentTotal: 10,
            paramsToUseForLimit: '',
            throttleEnabled: true,
            throttleOption: 'project'],
        pipelineTriggers([gerrit(silent:true,
                                 commentTextParameterMode: 'PLAIN',
                                 commitMessageParameterMode: 'PLAIN',
                                 customUrl: '',
                                 gerritProjects: [
                                     [pattern: 'frm2/nicos/nicos-core',
                                      compareType: 'PLAIN',
                                      disableStrictForbiddenFileVerification: false,
                                      branches: [[compareType: 'PLAIN', pattern: 'master'],
                                                 [compareType: 'PLAIN', pattern: 'release-3.1'],
                                                 [compareType: 'PLAIN', pattern: 'release-3.2'],
                                                 [compareType: 'PLAIN', pattern: 'release-3.3'],
                                                 [compareType: 'PLAIN', pattern: 'p3'],
                                                 ],
                                 ]],
                                 serverName: 'defaultServer',
                                 triggerOnEvents: [
                                        patchsetCreated(excludeDrafts: false,
                                                        excludeNoCodeChange: false,
                                                        excludeTrivialRebase: false),
                                        changeMerged(),
                                        commentAddedContains('@recheck')
                                        ]
                                    )])
    ])


// ********************************/


this.verifyresult = [:]

// ************* Function defs ***/

def parseLogs(parserConfigurations) {
    step([$class: 'WarningsPublisher',
          parserConfigurations: parserConfigurations,
          canComputeNew: false,
          canResolveRelativePaths: false,
          canRunOnFailed: true,
          defaultEncoding: 'UTF-8',
          excludePattern: '',
          includePattern: '',
          messagesPattern: '',
          healthy: '',
          unHealthy: '',
          failedTotalAll: '0',
          failedTotalHigh: '0',
          failedTotalLow: '0',
          failedTotalNormal: '0',
          unstableTotalAll: '0',
          unstableTotalHigh: '0',
          unstableTotalLow: '0',
          unstableTotalNormal: '0'])
}

def checkoutSource() {
    echo(GERRIT_PROJECT)
    deleteDir()
    checkout(
        changelog: true, poll: false,
        scm: [$class: 'GitSCM',
              branches: [[name: "$GERRIT_BRANCH"]],
              doGenerateSubmoduleConfigurations: false, submoduleCfg: [],
              userRemoteConfigs: [
                  [refspec: GERRIT_REFSPEC,
                   // use local mirror via git
                   url: 'file:///home/git/' + GERRIT_PROJECT
                   // use gerrit directly
                   //credentialsId: 'jenkinsforge',
                   //url: 'ssh://forge.frm2.tum.de:29418/' + GERRIT_PROJECT,
                  ]
              ],
              extensions: [
                  [$class: 'CleanCheckout'],
                  [$class: 'LocalBranch', localBranch: 'check'],
                  [$class: 'hudson.plugins.git.extensions.impl.BuildChooserSetting',
                   buildChooser: [$class: "com.sonyericsson.hudson.plugins.gerrit.trigger.hudsontrigger.GerritTriggerBuildChooser"]],
              ]
            ]
        )
    sh '''git describe'''
    sh '''#!/bin/bash
if [[ ! -d ciscripts ]] ;  then
    echo "Rebasing change to get ciscripts: If this fails, rebase manually!"
    git rebase -f -v origin/$GERRIT_BRANCH
fi'''
}

def publishGerrit(name, value) {
    gerritverificationpublisher([
        verifyStatusValue: value,
        verifyStatusName: name,
        verifyStatusCategory: 'test',
        verifyStatusReporter: 'jenkins',
        verifyStatusRerun: '@recheck'
    ])

}


def refreshVenv(venv='$NICOSVENV', checkupdates=false) {
    sh("./ciscripts/run_venvupdate.sh $venv")

    archiveArtifacts([allowEmptyArchive: true, artifacts: "pip-*.log"])
    if (checkupdates) {
        // currently only core requirements are checked
        def pconf = [
            [parserName: 'pip-output-error', pattern: 'pip-core*.log'],
            [parserName: 'pip-output-error-compile', pattern: 'pip-core*.log'],
            [parserName: 'pip-output-updated', pattern: 'pip-core*.log'],
        ]
        warnings([canComputeNew: false,
              canResolveRelativePaths: false,
              canRunOnFailed: true,
              failedTotalAll: '0',
              healthy: '0',
              parserConfigurations: pconf,
              unHealthy: '1',
        ])
    }
}

def runPylint() {
    verifyresult.put('pylint',0)
    try {
        withCredentials([string(credentialsId: 'GERRITHTTP', variable: 'GERRITHTTP')]) {
            refreshVenv()
            sh './ciscripts/run_pylint.sh'
            verifyresult.put('pylint', 1)
        }
    }
    catch (all) {
        verifyresult.put('pylint',-1)
    }
    echo "pylint: result=" + verifyresult['pylint']
    publishGerrit('pylint', verifyresult['pylint'])

    if (verifyresult['pylint'] < 0) {
        error('Failure in pylint')
    }
}

def runSetupcheck() {
    verifyresult.put('sc', 0)
    try {
        withCredentials([string(credentialsId: 'GERRITHTTP',
                                variable: 'GERRITHTTP')]) {
            refreshVenv()
            ansiColor('xterm') {
                sh './ciscripts/run_setupcheck.sh'
            }
            verifyresult.put('sc', 1)
        }
    }
    catch (all) {
        verifyresult.put('sc', -1)
    }
    echo "setupcheck: result=" + verifyresult['sc']
    publishGerrit('setupcheck',verifyresult['sc'])

    if (verifyresult['sc'] < 0) {
         error('Failure in setupcheck')
    }
}

def runTests(venv, pyver, withcov, checkpypiupdates=false) {
    refreshVenv(venv, checkpypiupdates)
    writeFile file: 'setup.cfg', text: """
[tool:pytest]
addopts = --junit-xml=pytest-${pyver}.xml
  --junit-prefix=$pyver""" + (withcov ? """
  --cov
  --cov-config=.coveragerc
  --cov-report=html:cov-$pyver
  --cov-report=term
""" : "")


    verifyresult.put(pyver, 0)
    try {
         timeout(10) {
           sh "./ciscripts/run_pytest.sh $venv"
           verifyresult.put(pyver, 1)
         } // timeout
    } catch(all) {
        verifyresult.put(pyver, -1)
    }

    echo "Test $pyver: result=" + verifyresult[pyver]
    publishGerrit('pytest-'+pyver, verifyresult[pyver])

    junit([allowEmptyResults: true,
           keepLongStdio: true,
           testResults: "pytest-${pyver}.xml"])
    if (withcov) {
        archiveArtifacts([allowEmptyArchive: true,
                          artifacts: "cov-$pyver/*"])
        publishHTML([allowMissing: true,
                     alwaysLinkToLastBuild: false,
                     keepAll: true,
                     reportDir: "cov-$pyver/",
                     reportFiles: 'index.html',
                     reportName: "Coverage ($pyver)"])
    }

    if (verifyresult[pyver] < 0) {
        error('Failure in test with ' + pyver)
    }
}

def runDocTest() {
    verifyresult.put('doc', 0)
    try {
        refreshVenv()
        sh './ciscripts/run_doctest.sh'
        archiveArtifacts([allowEmptyArchive: true,
                          artifacts: 'doc/build/latex/NICOS.*'])
        publishHTML([allowMissing: true,
                     alwaysLinkToLastBuild: true,
                     keepAll: true,
                     reportDir: 'doc/build/html',
                     reportFiles: 'index.html',
                     reportName: 'Nicos Doc (test build)'])

        verifyresult.put('doc', 1)
    } catch (all) {
        verifyresult.put('doc',-1 )
    }
    echo "Docs: result=" + verifyresult['doc']
    publishGerrit('doc', verifyresult['doc'])

    if (verifyresult['doc'] < 0) {
        error('Failure in doc test')
    }
}

// *************End Function defs ***/

// ************* Start main script ***/
timestamps {

node('master') {
    stage(name: 'checkout code: ' + GERRIT_PROJECT) {
        checkoutSource()
    }

    stage(name: 'prepare') {
        withCredentials([string(credentialsId: 'RMAPIKEY', variable: 'RMAPIKEY'), string(credentialsId: 'RMSYSKEY', variable: 'RMSYSKEY')]) {
            docker.image('localhost:5000/nicos-jenkins:xenial').inside(){
                sh  '''\
#!/bin/bash
export PYTHONIOENCODING=utf-8
~/tools2/bin/mlzrmupdater
'''
            }
        }
    }

u16 = docker.image('localhost:5000/nicos-jenkins:xenial')
u14 = docker.image('localhost:5000/nicos-jenkins:trusty')

parallel pylint: {
    stage(name: 'pylint') {
        u16.inside('-v /home/git:/home/git') {
                runPylint()
                parseLogs([[parserName: 'PyLint', pattern: 'pylint_*.txt']])
        }
    }
}, setup_check: {
    stage(name: 'Nicos Setup check') {
        u16.inside('-v /home/git:/home/git') {
                timeout(5) {
                    runSetupcheck()
                }
                parseLogs([
                    [parserName: 'nicos-setup-check-syntax-errors', pattern: 'setupcheck.log'],
                    [parserName: 'nicos-setup-check-errors-file', pattern: 'setupcheck.log'],
                    [parserName: 'nicos-setup-check-warnings', pattern: 'setupcheck.log'],
                ])
        }
    }
}, test_python2: {
    stage(name: 'Python2 tests')  {
        ws {
            checkoutSource()
            docker.image('localhost:5000/kafka').withRun() { kafka ->
                sleep(time:10, unit: 'SECONDS')  // needed to allow kafka to start
                sh "docker exec ${kafka.id} /opt/kafka_2.11-0.11.0.1/bin/kafka-topics.sh --create --topic test-flatbuffers --zookeeper localhost --partitions 1 --replication-factor 1"
                sh "docker exec ${kafka.id} /opt/kafka_2.11-0.11.0.1/bin/kafka-topics.sh --create --topic test-flatbuffers-history --zookeeper localhost --partitions 1 --replication-factor 1"
                u14.inside("-v /home/git:/home/git -e KAFKA_URI=kafka:9092  --link ${kafka.id}:kafka") {
                    runTests( '$NICOSVENV', 'python2', GERRIT_EVENT_TYPE == 'change-merged')
                }
            }
        }
    }
}, test_python2centos: {
    stage(name: 'Python2(centos) tests') {
        if (GERRIT_EVENT_TYPE == 'change-merged') {
            ws {
                checkoutSource()
                docker.image('localhost:5000/nicos-jenkins:centos6').inside('-v /home/git:/home/git') {
                    runTests('$NICOSVENV', 'python2-centos', false, true)
                }
            }
        }
    }
}, test_python3: {
    stage(name: 'Python3 tests') {
        ws {
            checkoutSource()
            u16.inside('-v /home/git:/home/git') {
                runTests('$NICOS3VENV', 'python3', GERRIT_EVENT_TYPE == 'change-merged')
            }
        }
    }
}, test_docs: {
    stage(name: 'Test docs') {
        docker.image('localhost:5000/nicos-jenkins:nicosdocs').inside(){
            runDocTest()
        }
    }
},
failFast: false

/*** set final vote **/
setGerritReview()
}
}
