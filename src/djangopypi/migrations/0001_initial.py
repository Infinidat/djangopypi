# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Classifier'
        db.create_table('djangopypi_classifier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('djangopypi', ['Classifier'])

        # Adding model 'Project'
        db.create_table('djangopypi_project', (
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('license', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('metadata_version', self.gf('django.db.models.fields.CharField')(default=1.0, max_length=64)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('home_page', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('download_url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('author_email', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('djangopypi', ['Project'])

        # Adding M2M table for field classifiers on 'Project'
        db.create_table('djangopypi_project_classifiers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['djangopypi.project'], null=False)),
            ('classifier', models.ForeignKey(orm['djangopypi.classifier'], null=False))
        ))
        db.create_unique('djangopypi_project_classifiers', ['project_id', 'classifier_id'])

        # Adding model 'Release'
        db.create_table('djangopypi_release', (
            ('upload_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('md5_digest', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('filetype', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('pyversion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='releases', to=orm['djangopypi.Project'])),
            ('platform', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('signature', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('distribution', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('djangopypi', ['Release'])

        # Adding unique constraint on 'Release', fields ['project', 'version', 'platform', 'distribution', 'pyversion']
        db.create_unique('djangopypi_release', ['project_id', 'version', 'platform', 'distribution', 'pyversion'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Classifier'
        db.delete_table('djangopypi_classifier')

        # Deleting model 'Project'
        db.delete_table('djangopypi_project')

        # Removing M2M table for field classifiers on 'Project'
        db.delete_table('djangopypi_project_classifiers')

        # Deleting model 'Release'
        db.delete_table('djangopypi_release')

        # Removing unique constraint on 'Release', fields ['project', 'version', 'platform', 'distribution', 'pyversion']
        db.delete_unique('djangopypi_release', ['project_id', 'version', 'platform', 'distribution', 'pyversion'])
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'djangopypi.classifier': {
            'Meta': {'object_name': 'Classifier'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'djangopypi.project': {
            'Meta': {'object_name': 'Project'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'author_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'classifiers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['djangopypi.Classifier']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'download_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'home_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'metadata_version': ('django.db.models.fields.CharField', [], {'default': '1.0', 'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': "orm['auth.User']"}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'djangopypi.release': {
            'Meta': {'unique_together': "(('project', 'version', 'platform', 'distribution', 'pyversion'),)", 'object_name': 'Release'},
            'distribution': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filetype': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5_digest': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'releases'", 'to': "orm['djangopypi.Project']"}),
            'pyversion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'signature': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'upload_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }
    
    complete_apps = ['djangopypi']
