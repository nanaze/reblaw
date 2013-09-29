#!/usr/bin/env python

import os
import html5lib
import shutil
import logging

import xml.dom

out_dir = '_out'

def _ShouldIgnoreFilename(filename):
  return filename.startswith('.') or filename.endswith('~')

def _Ignore(dir, files):
  return filter(_ShouldIgnoreFilename, files)  
    
def _CopyTree(dir):
  src = dir
  dest = os.path.join(out_dir, dir)
  shutil.copytree(src, dest, ignore=_Ignore) 

def _ReadFile(path):
  with open(path) as f:
    return f.read()
  
def _ParseDocument(content):
  return html5lib.parse(content, treebuilder='dom')

def _ParseDocumentFragment(content):
  return html5lib.parseFragment(content, treebuilder='dom')
  
def _CreateTemplateDom():
  return _ParseDocument(_ReadFile('templates/main.html'))

def _FindElementById(root, elem_id):
  for elem in _YieldElements(root):
    if elem.hasAttribute('id'):
      if elem_id == elem.getAttribute('id'):
        return elem

def _YieldElements(root):
  for node in _YieldNodes(root):
    if node.nodeType == xml.dom.Node.ELEMENT_NODE:
      yield node

def _YieldNodes(root):
  yield root
  for child in root.childNodes:
    for val in _YieldNodes(child):
      yield val
  
def _PopulateContent():

  for content_filename in os.listdir('content'):
    path = os.path.join('content', content_filename)
    if path.endswith('.html'):

      # We just recreate from disk as a DOM created by cloneNode(True) seems
      # not to reserialize correctly.
      template_dom = _CreateTemplateDom()
      content = _ReadFile(path)
      fragment = _ParseDocumentFragment(content)

      content_elem = _FindElementById(template_dom, 'content')
      content_elem.appendChild(fragment)

      s = html5lib.serializer.htmlserializer.HTMLSerializer(omit_optional_tags=False)
      walker = html5lib.treewalkers.getTreeWalker("dom")(template_dom)

      with open(os.path.join(out_dir, content_filename), 'w') as f:
        for item in s.serialize(walker):
          f.write(item.encode('ascii', 'xmlcharrefreplace'))

                
def main():
  logging.basicConfig(level=logging.INFO)

  logging.info('Starting site build...')
  
  script_dir = os.path.dirname(os.path.realpath(__file__))
  os.chdir(script_dir)
  
  if os.path.exists(out_dir):
    shutil.rmtree(out_dir)

  os.mkdir(out_dir)

  _CopyTree('styles')
  _CopyTree('js')
  _CopyTree('images')  

  _PopulateContent()

  logging.info('Build complete. Site written to %s' % out_dir)



if __name__ == '__main__':
  main()
