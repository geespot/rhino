//
//  DetailViewController.m
//  RestfulIOSClient
//
//  Created by 孔 令开 on 13-5-14.
//  Copyright (c) 2013年 Egibbon. All rights reserved.
//

#import "DetailViewController.h"
#import "APIClient.h"

@interface DetailViewController ()  {
    NSMutableArray* keys;
    NSMutableArray* values;
    int currentRow;
}

- (void)configureView;
@end

@implementation DetailViewController

- (void)dealloc
{
    [_detailItem release];
    [_detailDescriptionLabel release];
    [super dealloc];
}

#pragma mark - Managing the detail item

- (void)setDetailItem:(id)newDetailItem
{
    if (_detailItem != newDetailItem) {
        [_detailItem release];
        _detailItem = [newDetailItem retain];

        // Update the view.
        [self configureView];
    }
}

- (void)configureView
{
    // Update the user interface for the detail item.

    if (self.detailItem) {
        self.title = [self.detailItem objectForKey:@"name"];
        id doc = [self.detailItem objectForKey:@"doc"];
        if (doc != [NSNull null]){
            self.detailDescriptionLabel.text = doc;
        }
        
        if (keys)   {
            [keys release];
        }
        keys = [[NSMutableArray array]retain];

        if (values) {
            [values release];
        }
        values = [[NSMutableArray array]retain];
        
        for (NSString* param in [self.detailItem objectForKey:@"params"])   {
            if (![param isEqualToString:@"user"] && ![param isEqualToString:@"request"]){
                [keys addObject:[[param copy]autorelease]];
                [values addObject:@""];
            }
        }
        
        [self.tableView reloadData];
    }
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
    [self configureView];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
    }
    return self;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section    {
    return [keys count];
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath  {
    static NSString *CellIdentifier = @"Cell";
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier];
    if (cell == nil) {
        cell = [[[UITableViewCell alloc] initWithStyle:UITableViewCellStyleValue1 reuseIdentifier:CellIdentifier] autorelease];
    }
    cell.textLabel.text = [keys objectAtIndex:indexPath.row];
    cell.detailTextLabel.text = [values objectAtIndex:indexPath.row];

    return cell;
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    
    currentRow = indexPath.row;
    UIAlertView * alert = [[UIAlertView alloc] initWithTitle:nil
                                                     message:[keys objectAtIndex:indexPath.row]
                                                    delegate:self
                                           cancelButtonTitle:@"Cancel" otherButtonTitles:@"OK", nil];
    alert.alertViewStyle = UIAlertViewStylePlainTextInput;
    [alert show];
    [alert release];
}

- (void)alertView:(UIAlertView *)alertView clickedButtonAtIndex:(NSInteger)buttonIndex  {
    if (buttonIndex == 1)   {
        [values setObject:[[alertView textFieldAtIndex:0]text] atIndexedSubscript:currentRow];
        [self.tableView reloadData];
    }
}

- (IBAction)doTest:(id)sender   {
    NSDictionary* dict = [NSDictionary dictionaryWithObjects:values forKeys:keys];
    APIClientPromise* p = [[APIClient sharedClient]call_now:NO
                                                    apiName:[self.detailItem objectForKey:@"name"]
                                                     params:dict];
    [p done:^(int statusCode, id data, NSDictionary* headers){
        UIAlertView * alert = [[UIAlertView alloc] initWithTitle:@"调用成功"
                                                         message:[NSString stringWithFormat:@"%@", data]
                                                        delegate:nil
                                               cancelButtonTitle:@"OK" otherButtonTitles: nil];
        [alert show];
        [alert release];
    }];
    
    [p fail:^(int statusCode, id data, NSDictionary* headers){
        UIAlertView * alert = [[UIAlertView alloc] initWithTitle:@"调用失败"
                                                         message:[NSString stringWithFormat:@"%@", data]
                                                        delegate:nil
                                               cancelButtonTitle:@"OK" otherButtonTitles: nil];
        [alert show];
        [alert release];
    }];
    [p always:^(int statusCode, id data, NSDictionary* headers){
        NSLog(@"Calling %@ - %d: %@", [self.detailItem objectForKey:@"name"], statusCode, data);
    }];
}

							
@end
