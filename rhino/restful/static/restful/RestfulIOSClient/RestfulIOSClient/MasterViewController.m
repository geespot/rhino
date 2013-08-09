//
//  MasterViewController.m
//  RestfulIOSClient
//
//  Created by 孔 令开 on 13-5-14.
//  Copyright (c) 2013年 Egibbon. All rights reserved.
//

#import "MasterViewController.h"
#import "APIViewController.h"
#import "APIClient.h"

@interface MasterViewController () {
    NSArray* _doc;
}
@end

@implementation MasterViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        self.title = @"Modules";
    }
    return self;
}
							
- (void)dealloc
{
    [_apiViewController release];
    [super dealloc];
}

- (void) refresh {    
    APIClientPromise* p = [[APIClient sharedClient]help_now:NO];
    [p done:^(int statusCode, id data, NSDictionary* headers){
        _doc = [[data copy]autorelease];
        [self.tableView reloadData];
    }];
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    UIBarButtonItem *refreshButton =
    [[[UIBarButtonItem alloc] initWithBarButtonSystemItem:UIBarButtonSystemItemRefresh
                                                   target:self
                                                   action:@selector(refresh)] autorelease];
    self.navigationItem.rightBarButtonItem = refreshButton;

    [self refresh];
}



#pragma mark - Table View

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return [_doc count];
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *CellIdentifier = @"Cell";
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier];
    if (cell == nil) {
        cell = [[[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:CellIdentifier] autorelease];
        cell.accessoryType = UITableViewCellAccessoryDisclosureIndicator;
    }
    cell.textLabel.text = [[_doc objectAtIndex:indexPath.row]objectAtIndex:0];
    return cell;
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
    if (!self.apiViewController) {
        self.apiViewController = [[[APIViewController alloc] initWithNibName:@"APIViewController" bundle:nil] autorelease];
    }
    NSArray* rowData = [_doc objectAtIndex:indexPath.row];
    self.apiViewController.title = [rowData objectAtIndex:0];
    self.apiViewController.data = [[rowData objectAtIndex:1]objectForKey:@"api_list"];
    
    [self.navigationController pushViewController:self.apiViewController animated:YES];
}

@end
