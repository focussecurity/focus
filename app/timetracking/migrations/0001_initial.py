# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TypeOfTimeTracking'
        db.create_table('timetracking_typeoftimetracking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 9, 13, 23, 40, 51, 904146))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 9, 13, 23, 40, 51, 904178))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='typeoftimetracking_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='typeoftimetracking_edited', null=True, blank=True, to=orm['auth.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='typeoftimetracking_edited', null=True, blank=True, to=orm['core.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('timetracking', ['TypeOfTimeTracking'])

        # Adding model 'Timetracking'
        db.create_table('timetracking_timetracking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 9, 13, 23, 40, 51, 904146))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 9, 13, 23, 40, 51, 904178))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='timetracking_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='timetracking_edited', null=True, blank=True, to=orm['auth.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='timetracking_edited', null=True, blank=True, to=orm['core.Company'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Order'])),
            ('typeOfWork', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['timetracking.TypeOfTimeTracking'])),
            ('time_start', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('time_end', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('timetracking', ['Timetracking'])


    def backwards(self, orm):
        
        # Deleting model 'TypeOfTimeTracking'
        db.delete_table('timetracking_typeoftimetracking')

        # Deleting model 'Timetracking'
        db.delete_table('timetracking_timetracking')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contacts.contact': {
            'Meta': {'object_name': 'Contact'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 13, 23, 40, 51, 904146)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 13, 23, 40, 51, 904178)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'contact_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '80'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'orders.order': {
            'Meta': {'object_name': 'Order'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'order_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'orders'", 'symmetrical': 'False', 'to': "orm['contacts.Contact']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'order_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 13, 23, 40, 51, 904146)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 13, 23, 40, 51, 904178)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'order_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'participant': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'participants'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['projects.Project']"}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ordersWhereResponsible'", 'to': "orm['auth.User']"})
        },
        'projects.project': {
            'Meta': {'object_name': 'Project'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 13, 23, 40, 51, 904146)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 13, 23, 40, 51, 904178)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'project_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'timetracking.timetracking': {
            'Meta': {'object_name': 'Timetracking'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'timetracking_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'timetracking_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 13, 23, 40, 51, 904146)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 13, 23, 40, 51, 904178)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'timetracking_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Order']"}),
            'time_end': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'time_start': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'typeOfWork': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['timetracking.TypeOfTimeTracking']"})
        },
        'timetracking.typeoftimetracking': {
            'Meta': {'object_name': 'TypeOfTimeTracking'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'typeoftimetracking_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'typeoftimetracking_created'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 13, 23, 40, 51, 904146)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 9, 13, 23, 40, 51, 904178)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'typeoftimetracking_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['timetracking']
